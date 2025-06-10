import os
import unittest

from dotenv import load_dotenv
from qwik_tern.connection import get_connection_pool
from qwik_tern.logger.logger import setup_logger
from qwik_tern.models.db_config import DbConfig

logger = setup_logger(__name__)

load_dotenv()

class TestConnectionPool(unittest.TestCase):
    
    def test_get_connection_pool_with_empty_config(self):
        """Test that get_connection_pool returns None with empty config"""
        pool = get_connection_pool({})
        self.assertIsNone(pool)
        
    def test_get_connection_pool_with_none_config(self):
        """Test that get_connection_pool returns None with None config"""
        pool = get_connection_pool(None)
        self.assertIsNone(pool)
    
    def test_get_connection_pool_success(self):
        """Test that get_connection_pool returns a non-None pool with valid config"""
        mock_config = DbConfig(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user= os.getenv("DB_USER"),
            passw= os.getenv("DB_PASS"),
            db= os.getenv("DB_NAME")
        )
        # Note: This would require mocking the Pool class for proper unit testing
        # In a real test environment, you might use unittest.mock to mock the Pool class
        # For this example, we're just showing the test structure
        pool = get_connection_pool(mock_config)
        self.assertIsNotNone(pool)