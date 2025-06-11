import threading

from qwik_tern.models.global_config_model import GlobalConfigModel
from mysql.connector.pooling import MySQLConnectionPool


class Current:
    _thread_local = threading.local()
    
    @classmethod
    def setConfig(cls, globalConfigModel : GlobalConfigModel):
        cls._thread_local.config = globalConfigModel
    
    @classmethod
    def getConfig(cls) -> GlobalConfigModel:
        return cls._thread_local.config
    
    
    @classmethod
    def setConnectionPool(cls, pool : MySQLConnectionPool):
        cls._thread_local.cnx_pool = pool
        
    @classmethod
    def getConnectionPool(cls) -> MySQLConnectionPool:
        return cls._thread_local.cnx_pool