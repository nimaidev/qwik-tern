
from qwik_tern.logger.logger import setup_logger
from qwik_tern.constants import MYSQL_DATATYPES

logger = setup_logger(__name__)
class CreateTableHelper:
    def __init__(self, table_config : any):
        self.table_config = table_config
        self.sql_cmd = None
    
    def initialize(self):
        try:
            if self.table_config.get("name") is not None:
                if self.table_config.get("columns") is not None:
                    if self.__validate_columns():
                        self.__create_table()
                    else:
                        raise Exception("Invalid column configuration")
                else:
                    raise Exception("A table must have atleast one column")
            else:
                raise Exception("A table must have a name")
        except Exception as e:
            logger.error(f"{e}")
            
    def __create_table(self):
        logger.debug("CREATING TABLE")
        pass
    
    def __validate_columns(self):
        flag = False
        for column_config in self.table_config.get("columns"):
            logger.debug(self.table_config.get(column_config))
            if (column_config.get("name") is not None 
                and isinstance(column_config.get("name"), str)
                and column_config.get("type") is not None
                and isinstance(column_config.get("type"), str) 
                and any(column_config.get("type").startswith(dtype) for dtype in MYSQL_DATATYPES)):
                flag = True
        return flag
                
            
        