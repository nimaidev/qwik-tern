import unittest
from mysql.connector.pooling import MySQLConnectionPool
from utilities.connection import create_internal_db, get_connection_pool

class TestConnection(unittest.TestCase):

    def test_get_connection_pool(self):
        pool = get_connection_pool()
        self.assertIsInstance(pool, MySQLConnectionPool)
        self.assertEqual(pool.pool_name, "mysql_pool")
        self.assertEqual(pool.pool_size, 5)

    def test_create_internal_db(self):
        pool = get_connection_pool()
        con = pool.get_connection()
        cursor = con.cursor()

        # Ensure the table does not exist before running the test
        cursor.execute("DROP TABLE IF EXISTS db_changelog")
        con.commit()

        # Run the function to create the table
        create_internal_db()

        # Check if the table was created
        cursor.execute("SHOW TABLES LIKE 'db_changelog'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

        # Clean up
        cursor.execute("DROP TABLE IF EXISTS db_changelog")
        con.commit()
        cursor.close()
        con.close()

if __name__ == '__main__':
    unittest.main()