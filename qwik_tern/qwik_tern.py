import traceback
from mysql.connector.pooling import MySQLConnectionPool as Pool
from qwik_tern.config.config_global import GlobalConfig
from qwik_tern.logger.logger import setup_logger
from qwik_tern.models.db_config_model import DbConfig
from qwik_tern.parser.parse_file import ParseFiles
from qwik_tern.thread_local import Current

logger = setup_logger(__name__)

class QwikTern:
    
    def __init__(self, db_config: DbConfig):
        """
        Initialize the database utility with a connection pool.
        
        Args:
            db_config: Database configuration object
        """
        try:
            
            GlobalConfig.initialize()
            
            config = self.get_mysql_db_config(db_config)
            self.pool = Pool(**config)
            logger.info("Database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database connection pool: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    @staticmethod
    def initalize():
        logger.info(f"Root Dir: {Current.getConfig().root_dir}")
        file_parser = ParseFiles()
        file_parser.process_changelog_files()
    
    @staticmethod    
    def get_mysql_db_config(db_config: DbConfig) -> dict:
        """
        Convert database configuration to a format suitable for MySQL connection pool.
        
        Args:
            db_config: Database configuration object
            
        Returns:
            Dictionary with MySQL connection pool configuration
        """
        config = {
            'pool_name': 'tern_pool',
            'pool_size': 5,  # Adjust pool size as needed
            'host': db_config.host,
            'user': db_config.user,
            'password': db_config.passw,
            'database': db_config.db,
            'autocommit': True,
            'connect_timeout': 10
        }
        
        # Add port only if it's not None, otherwise MySQL will use the default port (3306)
        if db_config.port is not None:
            config['port'] = db_config.port
            
        return config
        
    
        
    def remove_initial_db(self):
        connection = None
        cursor = None
        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS TERNCHANGELOGS;")
            connection.commit()
        except Exception as e:
            logger.error(f"Error dropping table: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        
    def check_or_create_initial_db(self) -> bool:
        """
        Check if the TERNCHANGELOGMASTER table exists in the database
        """
        connection = None
        cursor = None
        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for easier column access
            
            # Get database name from the connection
            db_name = connection.database
            if isinstance(db_name, bytes):
                db_name = db_name.decode('utf-8')

            # THIS IS THE CRITICAL CHANGE:
            # Use %s as a placeholder and pass db_name as a tuple to cursor.execute()
            query = """
                SELECT COUNT(*)
                FROM information_schema.TABLES
                WHERE table_schema = %s 
                AND table_name = 'TERNCHANGELOGS'
            """
            cursor.execute(query, (db_name,)) # Pass the database name as a parameter

            result = cursor.fetchone()

            if isinstance(result, dict):
                # Try accessing by 'COUNT(*)' directly, or if that fails, by values
                exists = list(result.values())[0] > 0 if result else False
            elif isinstance(result, tuple):
                exists = result[0] > 0 if result else False
            else: # result is None or some other unexpected type
                exists = False
            if not exists:
                logger.info(f"Table exists check: {'Found' if exists else 'Not found'} in database '{db_name}'")
                logger.info("Creating default database as not exists")
                table_create_query = self.__get_table_creation_query()
                cursor.execute(table_create_query)
            return exists
        except Exception as e: # Catching generic Exception for logging, but specific errors are better
            logger.error(f"An error occurred during table existence check: {e}")
            logger.error(f"Error type: {type(e)}") # Print the type of exception
            logger.error(f"Traceback: {traceback.format_exc()}") # Print the full traceback
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close() # Returns connection to the pool
                
    def __get_table_creation_query(self)-> str:
        return """
                CREATE TABLE `TERNCHANGELOGS` (
                    `ID` varchar(255) NOT NULL,
                    `AUTHOR` varchar(255) NOT NULL,
                    `FILENAME` varchar(255) NOT NULL,
                    `DATEEXECUTED` datetime NOT NULL,
                    `ORDEREXECUTED` int NOT NULL,
                    `EXECTYPE` varchar(10) NOT NULL,
                    `CHECKSUM` varchar(35) DEFAULT NULL,
                    `DESCRIPTION` varchar(255) DEFAULT NULL,
                    `COMMENTS` varchar(255) DEFAULT NULL,
                    `TAG` varchar(255) DEFAULT NULL,
                    `DEPLOYMENT_ID` varchar(10) DEFAULT NULL
                );
            """
            