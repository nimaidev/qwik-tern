from pymysqlpool.pool import Pool
from qwik_tern.logger.logger import setup_logger
from qwik_tern.models.db_config import DbConfig

logger = setup_logger(__name__)

def get_connection_pool(config: DbConfig) -> Pool:
    logger.info("Connecting to server...")
    if not config:
        logger.error("No database configuration found...")
        return None
    try:
        mysql_pool = Pool(
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.passw,
            db=config.db
        )
        mysql_pool.init()
        logger.info("Connected to server...")
        return mysql_pool
    except Exception as e:
        logger.critical(f"Error: {e}")
        return None