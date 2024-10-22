import string
from mysql.connector.pooling import MySQLConnectionPool
from typing import Dict, Any
from qwik_tern.logger import setup_logger

logger = setup_logger(__name__)

def get_connection_pool(config: Dict[str, Any]) -> Any:
    logger.info("Connecting to server...")
    if not config:
        logger.error("No database configuration found...")
        return
    db_config = config
    try:
        mysql_pool = MySQLConnectionPool(
            pool_name="mysql_pool",
            pool_size=10,
            **db_config
        )
        logger.info("Connected to server...")
        return mysql_pool
    except Exception as e:
        logger.critical(f"Error: {e}")
        return None

def create_internal_db(cnxPool: MySQLConnectionPool) -> bool:
    logger.info("Creating internal database...")
    cnx = cnxPool.get_connection()
    cursor = cnx.cursor()
    try:
        logger.info("Executing SQL command to create db_changelog table...")
        query : string = """
         CREATE TABLE IF NOT EXISTS `db_changelog` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `change_id` VARCHAR(255) NOT NULL,
                `author` VARCHAR(255) NOT NULL,
                `checksum` VARCHAR(255) NOT NULL,
                `description` TEXT NOT NULL,
                `status` VARCHAR(10),
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        logger.info(f"Executing query: {query}")
        cursor.execute(query)
        logger.info("SQL command executed successfully.")
        cnx.commit()
        logger.info("Internal database created...")
        return True
    except Exception as e:
        logger.error(f"Error: {e}")
        return False
    finally:
        logger.info("Closing cursor and connection...")
        cursor.close()
        cnx.close()
        logger.info("Cursor and connection closed.")