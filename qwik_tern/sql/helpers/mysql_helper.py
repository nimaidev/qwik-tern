import sys
from qwik_tern.logger.logger import setup_logger
from qwik_tern.thread_local import Current

logger = setup_logger(__name__)

class MySQLHelper:
    def execute(self, raw_sql: str, params=None) -> bool:
        """
        Executes the given SQL statement with optional parameters.

        Args:
            raw_sql (str): The SQL statement to execute.
            params (tuple, optional): Parameters to pass to the SQL statement.

        Returns:
            bool: True if execution was successful, False otherwise.
        """
        cnx_pool = None
        connection = None
        cursor = None
        try:
            cnx_pool = Current.getConnectionPool()
            if cnx_pool is None:
                raise Exception("Unable to acquire connection pool")
            connection = cnx_pool.get_connection()
            cursor = connection.cursor()
            if params:
                cursor.execute(raw_sql, params)
            else:
                cursor.execute(raw_sql)
            connection.commit()
            logger.info("SUCCESS")
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Failed to execute SQL: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                
    def execute_count(self, raw_sql: str, params=None) -> int:
        """
        Executes the given SQL query and returns the count result.

        Args:
            raw_sql (str): The SQL query to execute.
            params (tuple, optional): Parameters to pass to the SQL query.

        Returns:
            int: The count result from the query, or 0 if execution failed.
        """
        cnx_pool = None
        connection = None
        cursor = None
        try:
            cnx_pool = Current.getConnectionPool()
            if cnx_pool is None:
                raise Exception("Unable to acquire connection pool")
            connection = cnx_pool.get_connection()
            cursor = connection.cursor()
            if params:
                cursor.execute(raw_sql, params)
            else:
                cursor.execute(raw_sql)
            
            # Get the count result
            result = cursor.fetchone()
            count = result[0] if result else 0
            
            connection.commit()
            logger.info(f"SUCCESS - Count: {count}")
            return count
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Failed to execute count SQL: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()