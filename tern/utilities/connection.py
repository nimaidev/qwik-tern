from mysql.connector.pooling import MySQLConnectionPool


from typing import Dict, Any

def get_connection_pool(config: Dict[str, Any]) -> Any:
    print("Connecting to server...")
    if not config:
        print("No database configuration found...")
        return
    db_config = config
    try:
        mysql_pool = MySQLConnectionPool(
            pool_name="mysql_pool",
            pool_size=10,
            **db_config
        )
        print("Connected to server...")
        return mysql_pool
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_internal_db(cnxPool : MySQLConnectionPool) -> bool:
    print("Creating internal database...")
    cnx = cnxPool.get_connection()
    cursor = cnx.cursor()
    try:
        # TODO: need not to create table if already exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `db_changelog` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `change_id` VARCHAR(255) NOT NULL,
                `author` VARCHAR(255) NOT NULL,
                `checksum` VARCHAR(255) NOT NULL,
                `description` TEXT NOT NULL,
                `status` VARCHAR(10) DEFAULT 1,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
        
        cnx.commit()
        print("Internal database created...")
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        cnx.close()
    return True
