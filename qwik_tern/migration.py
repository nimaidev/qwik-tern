import string
import hashlib
import pandas as pd
from qwik_tern.connection import MySQLConnectionPool
import sys

from qwik_tern.logger import setup_logger

logger = setup_logger(__name__)

def read_migration_from_file(file_name: string) -> pd.Series:
    try:
        changes : pd.Series = pd.read_json(file_name).changeSet
        return changes
    except Exception as e:
        logger.critical(f"Error: {e}")
        return None

def run_default_migration(migration_filename: string, cnx_pool: MySQLConnectionPool) -> bool:
    changes : pd.Series = read_migration_from_file(migration_filename)
    if changes is None:
        logger.info("No changes found in the migration file.")
        sys.exit("Terminating program due to error reading the migration file.")
    _process_migration(cnx_pool=cnx_pool, changes=changes)
    return True

def run_migration_down(migration_filename: string, cnx_pool: MySQLConnectionPool) -> bool:
    changes = read_migration_from_file(migration_filename)
    if changes is None:
        logger.info("No changes found in the migration file.")
        sys.exit("Terminating program due to error reading the migration file.")
        return False
    return _process_migration_down(cnx_pool, changes)

def _process_migration_down(cnx_pool: MySQLConnectionPool, changes: pd.DataFrame) -> bool:
    try:
        con = cnx_pool.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute("""SELECT change_id FROM db_changelog ORDER BY id DESC LIMIT 1""")
            id = cursor.fetchone()[0]
            if id is None:
                logger.info("No change ID found in the db to migrate down")
                return False
            migration = ""
            for change in changes:
                if change.get("id") == id:
                    migration = change.get("migrateDown")
                    break
            logger.info("Migrating doen to change id ", id)
            logger.info("Query to migrating down: ", migration)
            if migration is None:
                logger.info("No down migration script found for id: %d " % id)
                return False
            cursor.execute(migration)
            cursor.execute("DELETE FROM db_changelog WHERE change_id = %s", (id,))
            logger.info("Migration down completed successfully for id: %d" % id)
            con.commit()
            cursor.close()
            con.close()
            return True
        except Exception as e:
            logger.critical(f"Error: {e}")
            return False
    except Exception as e:
        logger.critical(f"Error: {e}")
        return False

def _process_migration(cnx_pool: MySQLConnectionPool, changes: pd.DataFrame) -> bool:
    ids = changes.apply(lambda x: x["id"])
    duplicate_ids = ids[ids.duplicated()]
    if not duplicate_ids.empty:
        logger.critical("Duplicate IDs found: %s", duplicate_ids.tolist())
        sys.exit("Terminating program due to duplicate IDs.")
    else:
        logger.info("No duplicate IDs found")
    
    try:
        con = cnx_pool.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute("""SELECT * FROM db_changelog""")
            db_data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            data = pd.DataFrame(db_data, columns=columns)
            
            for change in changes:
                keyFile = change.get("id") + change.get("author")
                if change.get("check") is not None:
                    exists = _check_Query_Exectuion(cnx_pool, change)
                    if exists:
                        logger.warning("Changeset already exists.")
                        query = _get_changelog_insert_query(
                            change.get("id"),
                            change.get("author"),
                            _calculate_checksum(change.get("migrateUp")),
                            change.get("description"),
                            "SKIP"
                        )
                        if not _check_if_entry_exists(change.get("id"), change.get("author"), cnx_pool):
                            _add_entry_to_changelog_table(query, cnx_pool)
                        continue
                for _, row in data.iterrows():
                    keyDb = row["change_id"] + row["author"]
                    if keyFile == keyDb:
                        if _compare_checksum(row["checksum"], change.get("migrateUp")):
                            continue
                        else:
                            logger.critical("Invalid Checksum!!! previous checksum: %s current checksum:%s ", row["checksum"], _calculate_checksum(change.get("migrateUp")))
                            sys.exit("Terminating program due to checksum mismatch.")
                        continue
                _insert_data(cnx_pool, change)
                continue
        finally:
            cursor.close()
            con.close()
    except Exception as e:
        logger.critical(f"Error: {e}")
        return False

def _check_Query_Exectuion(cnx_pool: MySQLConnectionPool, change: pd.DataFrame) -> bool:
    try:
        con = cnx_pool.get_connection()
        cursor = con.cursor()
        try:
            checkQuery: str = change.get("check").strip()
            if not checkQuery.startswith("SELECT"):
                logger.critical("Invalid Check Query!!!")
                sys.exit("Terminating program due to invalid check query. Should Always start with SELECT")
            cursor.execute(change.get("check"))
            result = cursor.fetchone()
            if result[0] > 0:
                logger.warning("Changeset already exists.")
                return True
            else:
                logger.warning("Record not found")
                return False
        except Exception as e:
            logger.critical(f"Error: {e}")
            return False
        finally:
            cursor.close()
            con.close()
    except Exception as e:
        logger.critical(f"Error: {e}")
        return False

def _insert_data(cnx_pool, change):
    try:
        con = cnx_pool.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM db_changelog 
                WHERE change_id = %s AND author = %s
            """, (change.get("id"), change.get("author")))
            
            result = cursor.fetchone()
            if result[0] > 0:
                logger.warning("Record already exists.")
                return False
            
            status = False
            logger.info("Migration Up: %s", change.get("migrateUp"))
            try:
                cursor.execute(change.get("migrateUp"))
                status = True
            except Exception as e:
                status = False
            statusText = "SUCCESS" if status else "FAILED"
            
            query = _get_changelog_insert_query(change.get("id"), change.get("author"), _calculate_checksum(change.get("migrateUp")), change.get("description"), statusText)
            
            cursor.execute(query)
            con.commit()
        except Exception as e:
            logger.critical(f"Error: {e}")
            return False
        finally:
            cursor.close()
            con.close()
        return True
    except Exception as e:
        logger.critical(f"Error: {e}")
        return False

def _get_changelog_insert_query(change_id: string, author: string, checksum: string, description: string, status: string) -> string:
    return f"""
        INSERT INTO db_changelog (change_id, author, checksum, description, status)
        VALUES ('{change_id}', '{author}', '{checksum}', '{description}', '{status}');
    """

def _check_if_entry_exists(change_id: string, author: string, cnx: MySQLConnectionPool) -> bool:
    try:
        con = cnx.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM db_changelog 
                WHERE change_id = %s AND author = %s
            """, (change_id, author))
            result = cursor.fetchone()
            return result[0] > 0
        finally:
            cursor.close()
            con.close()
    except Exception as e:
        logger.critical(f"Error: {e}")
        return False

def _add_entry_to_changelog_table(query: string, cnx: MySQLConnectionPool) -> bool:
    try:
        con = cnx.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute(query)
            con.commit()
            return True
        except Exception as e:
            logger.critical(f"Error: {e}")
            return False
        finally:
            cursor.close()
            con.close()
    except Exception as e:
        logger.critical(f"Error: {e}")
        return False

def _calculate_checksum(changeText: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(changeText.encode('utf-8'))
    return sha256.hexdigest()

def _compare_checksum(checksum: str, changeText: str) -> bool:
    return checksum == _calculate_checksum(changeText)