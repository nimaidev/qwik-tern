
import sys
from qwik_tern.logger.logger import setup_logger
from qwik_tern.sql.helpers.create_table_helper import CreateTableHelper
from qwik_tern.sql.helpers.mysql_helper import MySQLHelper


TERN_CMD_LIST =[
    "sql",
    "createTable"
]

logger = setup_logger(__name__)
class ChangelogCommandHandler:
    def __init__(self):
        pass
    
    def handle(self, changes : any):
        try:
            # Get the first key name
            if isinstance(changes, dict) and len(changes) > 0:
                cmd = next(iter(changes))
                self.handle_cmd(cmd=cmd, data=changes.get(cmd))
            elif isinstance(changes, list) and len(changes) > 0:
                for change in changes:
                    if isinstance(change, dict) and len(change) > 0:
                        cmd = next(iter(change))
                        self.handle_cmd(cmd=cmd, data=change.get(cmd))
                    else:
                        raise Exception("Invalid command format in changes list")
            else:
                raise Exception("No commands found in changes")
        except Exception as e:
            logger.error(f"{e}")   
    
    def handle_cmd(self, cmd :str, data: any):
        try:
            if cmd in TERN_CMD_LIST:
                match cmd:
                    case "sql":
                        logger.debug("SQL COMMAND FOUND")
                        logger.info(f"command key: {cmd} Data : {data}")
                        
                        if data is None or not isinstance(data, str):
                            raise Exception(f"INVALID sql : {data}")
                        mysql_helper = MySQLHelper()
                        return mysql_helper.execute(raw_sql=data)

                    case "file":
                        # TODO: LOGIC NEEDS TO BE APPLIED
                        logger.debug("FILE command found")
                        return True
                    case "createTable":
                        logger.debug("[ADD TABLE] COMMAND FOUND")
                        createTableHelper = CreateTableHelper(data)
                        createTableHelper.initialize()
                    case _:
                        # Default case
                        raise Exception("No valid command found")
                        
            else:
                raise Exception(f"Invalid TERN changelog Command: {cmd}")
        except Exception as e:
            logger.error(f"{e}")
            sys.exit(0)
            
        
        
    