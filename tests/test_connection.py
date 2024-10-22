import unittest
from mysql.connector.pooling import MySQLConnectionPool
from qwik_tern.connection import get_connection_pool, create_internal_db
from qwik_tern.logger import setup_logger
from qwik_tern.migration import run_default_migration

logger = setup_logger(__name__)
class TestConnection(unittest.TestCase):
    db_config = {
        'host': 'localhost',
        'port': '3306',
        'user': 'remote',
        'password': 'Nimai@123',
        'database': 'ai_service',
        'auth_plugin': 'mysql_native_password'
    }

    def test_get_connection_pool(self):

        logger.info("Starting test_get_connection_pool")
        pool: MySQLConnectionPool = get_connection_pool(self.db_config)
        self.assertIsNotNone(pool)
        logger.info("Ending test_get_connection_pool")

    # def test_create_internal_db(self):
    #     logger.info("Starting test_create_internal_db")
    #     pool = get_connection_pool(self.db_config)
    #     con = pool.get_connection()
    #     cursor = con.cursor()
    #     cursor.execute("DROP TABLE IF EXISTS db_changelog")
    #     con.commit()

    #     # Run the function to create the table
    #     create_internal_db(pool)

    #     # Check if the table was created
    #     cursor.execute("SHOW TABLES LIKE 'db_changelog'")
    #     result = cursor.fetchone()
    #     self.assertIsNotNone(result)

        
    #     status = run_default_migration(migration_filename ="changes.json", cnx_pool = pool)
    #     self.assertTrue(status)
    #     # Clean up
    #     cursor.execute("DROP TABLE IF EXISTS db_changelog")
    #     con.commit()
        
    #     logger.info("Ending test_create_internal_db")

if __name__ == '__main__':
    unittest.main()