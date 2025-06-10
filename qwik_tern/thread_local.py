import threading

from qwik_tern.models.global_config_model import GlobalConfigModel


class Current:
    _thread_local = threading.local()
    
    @classmethod
    def setConfig(cls, globalConfigModel : GlobalConfigModel):
        cls._thread_local.config = globalConfigModel
    
    @classmethod
    def getConfig(cls) -> GlobalConfigModel:
        return cls._thread_local.config