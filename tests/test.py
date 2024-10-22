


from qwik_tern.connection import get_connection_pool


db_config = {
    'host': 'localhost',
    'port': '3306',
    'user': 'remote',
    'password': 'Nimai@123',
    'database': 'ai_service',
    'auth_plugin': 'mysql_native_password'
}


if __name__ == "__main__":
    con = get_connection_pool(db_config)