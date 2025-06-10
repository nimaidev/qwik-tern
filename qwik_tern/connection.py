from mysql.connector.pooling import MySQLConnectionPool
from qwik_tern.logger.logger import setup_logger
from qwik_tern.models.db_config import DbConfig

logger = setup_logger(__name__)

def get_connection_pool(config: DbConfig) -> MySQLConnectionPool:
    logger.info("Connecting to server...")
    if not config:
        logger.error("No database configuration found...")
        return None
    try:
        mysql_pool = MySQLConnectionPool(
            pool_size=5,
            pool_name="qwik_tern_pool",
            **config)
        logger.info("Connected to server...")
        return mysql_pool
    except Exception as e:
        logger.critical(f"Error: {e}")
        return None