# Tern🐧 - MySQL Versioning for Python

This project is a database migration tool that helps manage and apply database schema changes. It uses a JSON file to define the changes and applies them to a MySQL database. It is named after a bird called [Arctic Tern](https://en.wikipedia.org/wiki/Arctic_tern) which can migrate the longest distance. Yearly migration can range from 44,000 miles to 59,000 miles.


### Files

- `changes.json`: Contains the list of database changes to be applied.
- `connection.py`: Manages the database connection pool.
- `main.py`: Entry point for running the migration scripts.
- `Makefile`: Contains commands to run the project.
- `migration.py`: Contains functions to process migrations, calculate checksums, and insert data into the database.
- `requirement.txt`: Lists the Python dependencies for the project.
- `venv/`: Virtual environment directory.

## Setup

1. **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    ```

2. **Activate the Virtual Environment**:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirement.txt
    ```

## Usage

### Running Migrations

To run the migrations, use the [main.py](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CPython%5C%5Ctern%5C%5Cmain.py%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmain.py%22%2C%22scheme%22%3A%22file%22%7D%7D) script with the appropriate arguments.

- **Migrate Up**:
    ```sh
    python main.py --migrate up
    ```

- **Migrate Down**:
    ```sh
    python main.py --migrate down
    ```

### Makefile

You can also use the [Makefile](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CPython%5C%5Ctern%5C%5CMakefile%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2FMakefile%22%2C%22scheme%22%3A%22file%22%7D%7D) to run the project:

- **Run the Project**:
    ```sh
    make run
    ```

## Code Overview

### [connection.py](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CPython%5C%5Ctern%5C%5Cconnection.py%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fconnection.py%22%2C%22scheme%22%3A%22file%22%7D%7D)

- [`get_connection_pool()`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fconnection.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A3%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A3%2C%22character%22%3A43%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmigration.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A8%2C%22character%22%3A23%7D%7D%5D%2C%22a566a76a-77ec-4bb4-a3ec-a5469b4283f6%22%5D "Go to definition"): Returns a MySQL connection pool.
- [`create_internal_db()`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fconnection.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A26%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A3%2C%22character%22%3A23%7D%7D%5D%2C%22a566a76a-77ec-4bb4-a3ec-a5469b4283f6%22%5D "Go to definition"): Creates the internal database and the [`db_changelog`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fconnection.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A34%2C%22character%22%3A40%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmigration.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A25%2C%22character%22%3A48%7D%7D%5D%2C%22a566a76a-77ec-4bb4-a3ec-a5469b4283f6%22%5D "Go to definition") table if it doesn't exist.

### [migration.py](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CPython%5C%5Ctern%5C%5Cmigration.py%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmigration.py%22%2C%22scheme%22%3A%22file%22%7D%7D)

- [`process_migration_down(cnx_pool)`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A4%2C%22character%22%3A41%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmigration.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A19%2C%22character%22%3A4%7D%7D%5D%2C%22a566a76a-77ec-4bb4-a3ec-a5469b4283f6%22%5D "Go to definition"): Processes the down migration by one change.
- [`process_migration(cnx_pool)`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A4%2C%22character%22%3A22%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmigration.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A58%2C%22character%22%3A4%7D%7D%5D%2C%22a566a76a-77ec-4bb4-a3ec-a5469b4283f6%22%5D "Go to definition"): Processes the up migration by applying all changes from the [changes.json](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CPython%5C%5Ctern%5C%5Cchanges.json%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fchanges.json%22%2C%22scheme%22%3A%22file%22%7D%7D) file.
- [`insert_data(cnx_pool, change)`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmigration.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A95%2C%22character%22%3A8%7D%7D%5D%2C%22a566a76a-77ec-4bb4-a3ec-a5469b4283f6%22%5D "Go to definition"): Inserts a change record into the [`db_changelog`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fconnection.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A34%2C%22character%22%3A40%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmigration.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A25%2C%22character%22%3A48%7D%7D%5D%2C%22a566a76a-77ec-4bb4-a3ec-a5469b4283f6%22%5D "Go to definition") table.
- [`calculate_checksum(changeText)`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmigration.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A88%2C%22character%22%3A110%7D%7D%5D%2C%22a566a76a-77ec-4bb4-a3ec-a5469b4283f6%22%5D "Go to definition"): Calculates the SHA-256 checksum of a change text.
- [`compare_checksum(checksum, changeText)`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmigration.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A84%2C%22character%22%3A19%7D%7D%5D%2C%22a566a76a-77ec-4bb4-a3ec-a5469b4283f6%22%5D "Go to definition"): Compares the given checksum with the calculated checksum of a change text.
- [`read_migration_from_file(file_name)`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A4%2C%22character%22%3A65%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmigration.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A13%2C%22character%22%3A4%7D%7D%5D%2C%22a566a76a-77ec-4bb4-a3ec-a5469b4283f6%22%5D "Go to definition"): Reads migration data from a YAML file.

### [main.py](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CPython%5C%5Ctern%5C%5Cmain.py%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmain.py%22%2C%22scheme%22%3A%22file%22%7D%7D)

- Entry point for the migration tool.
- Parses command-line arguments to determine whether to migrate up or down.
- Calls the appropriate functions from [migration.py](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CPython%5C%5Ctern%5C%5Cmigration.py%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fmigration.py%22%2C%22scheme%22%3A%22file%22%7D%7D) to process the migrations.

## Example [changes.json](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CPython%5C%5Ctern%5C%5Cchanges.json%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FE%3A%2FPython%2Ftern%2Fchanges.json%22%2C%22scheme%22%3A%22file%22%7D%7D)

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