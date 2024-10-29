# Qwik-Tern🐧 - MySQL Versioning for Python

## Overview
`qwik-tern` is a database migration tool that helps manage and apply schema changes to a MySQL database. It simplifies the process of updating database structures by defining changes in a single JSON file. Named after the Arctic Tern, a bird famous for its long migration journeys—spanning from 44,000 to 59,000 miles each year. `qwik-tern` enables efficient, reliable migrations for projects that require robust database evolution.

## Installation

To install `qwik-tern` into an existing Python project, use `pip`:

```bash
pip install qwik-tern
```

Or, download the repository and run `qwik-tern` as a standalone application (see [Standalone Setup](#standalone-setup) for instructions).

## Usage

### In an Existing Python Project

Once installed, you can configure and use `qwik-tern` to manage your database migrations programmatically.

#### Example Code

```python
import qwik_tern

# Database configuration
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'database': 'your_database'
}

# Get the connection pool
cnx = qwik_tern.get_connection_pool(config=db_config)

# Create the internal database
qwik_tern.create_internal_db(cnx)

# Run migrations from the migration file
qwik_tern.run_default_migration(migration_filename="./changes.json", cnx_pool=cnx)
```

### `changes.json` File

The `changes.json` file should be located in the same directory as `main.py` and contains the list of migrations. Each migration has details on `migrateUp` (applying changes) and `migrateDown` (reverting changes). 

#### Example `changes.json` Structure

```json
{
    "changeSet": [
        {
            "id": "1",
            "author": "John Doe",
            "description": "Initial version",
            "date": "2019-01-01",
            "comment": "Initial version",
            "migrateUp": "CREATE TABLE my_table (id INT PRIMARY KEY, name VARCHAR(255));",
            "migrateDown": "DROP TABLE my_table;"
        },
        {
            "id": "2",
            "author": "John Doe",
            "description": "Add column",
            "date": "2019-01-02",
            "comment": "Add column",
            "migrateUp": "ALTER TABLE my_table ADD COLUMN age INT;",
            "migrateDown": "ALTER TABLE my_table DROP COLUMN age;"
        }
    ]
}
```

### Standalone Setup

To use `qwik-tern` as a standalone application, follow these setup instructions.

1. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**

   - **On Windows:**
     ```bash
     .\venv\Scripts\activate
     ```
   - **On macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Running Migrations

The main script, `main.py`, provides commands for running database migrations.

### Migration Commands

To migrate up or down, use the following commands:

- **Migrate Up**

  ```bash
  python main.py --migrate up
  ```

- **Migrate Down**

  ```bash
  python main.py --migrate down
  ```

These commands apply or roll back changes defined in the `changes.json` file.

---

This expanded documentation provides clear instructions for creating and using `changes.json`, ensuring that users know where to place it and how to format it.

---
In case you want to contribute please read our [Contribution Guidelines](readme/contributor-guidelines.md).