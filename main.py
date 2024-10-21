

import argparse
from connection import create_internal_db, get_connection_pool
from migration import process_migration, process_migration_down, read_migration_from_file


cnx_pool = get_connection_pool()


# Argument
# 1. change file Name
# 2. migrate up
# 3. migrate down
if __name__ == '__main__':
    print('Hello, World!')
    create_internal_db()
    
    parser = argparse.ArgumentParser(description='Process migration scripts.')
    
    parser.add_argument('--migrate', type=str, required=True, help='The migrate up script')

    args = parser.parse_args()
    print(args)
    status = False
    if args.migrate.lower() == "up":
        print("Running UP changes")
        status = process_migration(cnx_pool)
        if status:
            print("Migration completed successfully")
        else:
            print("Migration failed")
    elif args.migrate.lower() == "down":
        print("Running DOWN migration By One change")
        # Example: Handle rollback by reading and processing a down migration file
        status = process_migration_down(cnx_pool)
        if status:
            print("Migration completed successfully")
        else:
            print("Migration failed")
    else:
        print(f"Unknown migration direction, try: python main.py --help")