import unittest
from mysql.connector.pooling import MySQLConnectionPool
from connection import get_connection_pool, create_internal_db

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
        pool = get_connection_pool(self.db_config)
        self.assertIsNotNone(pool)

    def test_create_internal_db(self):
        pool = get_connection_pool(self.db_config)
        con = pool.get_connection()
        cursor = con.cursor()
        cursor.execute("DROP TABLE IF EXISTS db_changelog")
        con.commit()

        # Run the function to create the table
        create_internal_db(pool)

        # Check if the table was created
        cursor.execute("SHOW TABLES LIKE 'db_changelog'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

        # Clean up
        cursor.execute("DROP TABLE IF EXISTS db_changelog")
        con.commit()

if __name__ == '__main__':
    unittest.main()