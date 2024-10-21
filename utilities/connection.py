from mysql.connector.pooling import MySQLConnectionPool


def get_connection_pool() -> any:
    print("Connecting to server...")
    db_config = {
        'host': '10.10.10.11',
        'port': '3306',
        'user' : "remote",
        'password' : "Nimai@123",
        'database' : "ai-service",
        'auth_plugin': 'mysql_native_password'
    }

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

def create_internal_db() -> bool:
    cnx_pool = get_connection_pool()
    print("Creating internal database...")
    cnx = cnx_pool.get_connection()
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
