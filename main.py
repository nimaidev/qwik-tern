import os
import time

from dotenv import load_dotenv
from qwik_tern.database_utility import DbUtility
from qwik_tern.logger.logger import setup_logger
from qwik_tern.models.db_config_model import DbConfig

logger = setup_logger(__name__)
load_dotenv()

def main():
    config = DbConfig(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user= os.getenv("DB_USER"),
            passw= os.getenv("DB_PASS"),
            db= os.getenv("DB_NAME")
        )
    db_utility = DbUtility(config)
    db_utility.remove_initial_db()
    time.sleep(2)
    db_utility.check_or_create_initial_db()
if __name__ == '__main__':
    main()

