
from pymysqlpool.pool import Pool


class DbUtility:
    def __init__(self, pool : Pool):
        self.pool = pool
    
    def __create_initial_db() -> bool:
        return False