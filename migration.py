


import string
import hashlib
import pandas as pd
import yaml

from connection import get_connection_pool
import sys

cnx_pool = get_connection_pool()

def read_migration_from_file(file_name : string):
    with open(file_name, 'r') as file:
        return yaml.safe_load(file)



def process_migration_down(cnx_pool) -> bool:
    changes = pd.read_json("changes.json").changeSet
    #  get the last change ID from the db
    try:
        con = cnx_pool.get_connection()
        cursor = con.cursor()
        cursor.execute("""SELECT change_id FROM db_changelog ORDER BY id DESC LIMIT 1""")
        id = cursor.fetchone()[0]
        if id == None:
            print("No change ID found in the db to migrate down")
            return False
        print("Last change ID: ", id)
        # get the down migration script from the changes.json file
        # print("Changes: ", changes)
        migration = ""
        for change in changes:
            if change.get("id") == id:
                migration = change.get("migrateDown")
                break
        print("Change: ", migration)
        # execute the down migration script
        if migration==None:
            print("No down migration script found for id: %d "% id)
            return False
        
        cursor.execute(migration)
        cursor.execute("DELETE FROM db_changelog WHERE change_id = %s", (id,))
        print("Migration down completed successfully for id: %d"% id)
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        con.close()    
    
        
    
    

def process_migration(cnx_pool):
    changes = pd.read_json("changes.json").changeSet
    # get all ids and check for duplicates
    ids = changes.apply(lambda x: x["id"])
    duplicate_ids = ids[ids.duplicated()]
    if not duplicate_ids.empty:
        print("Duplicate IDs found:", duplicate_ids.tolist())
        sys.exit("Terminating program due to duplicate IDs.")
    else:
        print("No duplicate IDs found: ", duplicate_ids.tolist())
    # cnx_pool = get_connection_pool()
    con = cnx_pool.get_connection()
    cursor = con.cursor()

    cursor.execute("""SELECT * FROM db_changelog""")
    db_data =  cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = pd.DataFrame(db_data, columns=columns)
    
    # Get the change Id which are not there in the db
    
    for change in changes:
        keyFile = change.get("id")+change.get("author")
        for _, row in data.iterrows():
            keyDb = row["change_id"]+row["author"]
            if keyFile == keyDb:
                if compare_checksum(row["checksum"], change.get("migrateUp")):
                    print("Checksum matched")
                    continue
                else:
                    print("Invalid Checksum!!! \nprevious checksum: ", row["checksum"], "current checksum: ", calculate_checksum(change.get("migrateUp")))
                    sys.exit("Terminating program due to checksum mismatch.")    
                # check if key File is not present in the db
                # then insert the data
                continue
            else:
                pass
        insert_data(cnx_pool, change)
        continue
                
            


def insert_data(cnx_pool, change):
    con = cnx_pool.get_connection()
    cursor = con.cursor()
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM db_changelog 
            WHERE change_id = %s AND author = %s
        """, (change.get("id"), change.get("author")))
        
        result = cursor.fetchone()
        if result[0] > 0:
            print("Record already exists.")
            return False
        
        # execute the SQL query from the changeSet
        status = False
        print("Migration Up: ", change.get("migrateUp"))
        try:
            cursor.execute(change.get("migrateUp"))
            status = True
        except Exception as e:
            status = False
        statusText = "SUCCESS" if status else "FAILED"
        
        cursor.execute("""
            INSERT INTO db_changelog (change_id, author, checksum, description, status)
            VALUES (%s, %s, %s, %s, %s)
            """, (
                change.get("id"), 
                change.get("author"), 
                calculate_checksum(change.get("migrateUp")), 
                change.get("description"), 
                statusText
            )
        )
        con.commit()
    except Exception as e:
        print(f"Error: {e}")
        return False
    con.close()
    return True



def calculate_checksum(changeText: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(changeText.encode('utf-8'))
    return sha256.hexdigest()

def compare_checksum(checksum: str, changeText: str) -> bool:
    return checksum == calculate_checksum(changeText)