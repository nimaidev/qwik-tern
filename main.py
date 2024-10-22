import argparse
from qwik_tern.connection import create_internal_db, get_connection_pool
from qwik_tern.logger import setup_logger
from qwik_tern.migration import run_default_migration, run_migration_down

logger = setup_logger(__name__)

# Argument
# 1. change file Name
# 2. migrate up
# 3. migrate down
if __name__ == '__main__':
    logger.info('Hello, World!')

    # Define the database configuration
    db_config = {
        'host': 'localhost',
        'port': '3306',
        'user': 'remote',
        'password': 'Nimai@123',
        'database': 'ai_service',
        'auth_plugin': 'mysql_native_password'
    }

    # Initialize the connection pool
    cnx_pool = get_connection_pool(db_config)
    if not cnx_pool:
        logger.critical("Failed to create connection pool. Exiting.")
        exit(1)

    # Create the internal database
    create_internal_db(cnx_pool)

    parser = argparse.ArgumentParser(description='Process migration scripts.')
    parser.add_argument('--migrate', type=str, required=True, help='The migrate up script')

    args = parser.parse_args()
    status = False
    if args.migrate.lower() == "up":
        logger.info("Running changes for migration up..")
        status = run_default_migration(migration_filename="changes.json", cnx_pool=cnx_pool)
        if status:
            logger.info("Migration completed successfully")
        else:
            logger.critical("Migration failed")
    elif args.migrate.lower() == "down":
        logger.info("Running DOWN migration By One change")
        # Example: Handle rollback by reading and processing a down migration file
        status = run_migration_down(migration_filename="changes.json", cnx_pool=cnx_pool)
        if status:
            logger.info("Migration completed successfully")
        else:
            logger.critical("Migration failed")
    else:
        logger.warning(f"Unknown migration direction, try: python main.py --help")