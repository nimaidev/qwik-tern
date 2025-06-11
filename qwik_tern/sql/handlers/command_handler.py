
from qwik_tern.logger.logger import setup_logger
from qwik_tern.sql.helpers.create_table_helper import CreateTableHelper


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
            else:
                raise Exception("No commands found in changes")
        except Exception as e:
            logger.error(f"{e}")   
    
    def handle_cmd(self, cmd :str, data: any):
        try:
            if cmd in TERN_CMD_LIST:
                logger.info(f"command key: {cmd} Data : {data}")
                match cmd:
                    case "sql":
                        logger.debug("SQL COMMAND FOUND")
                        # TODO: LOGIC NEEDS TO BE APPLIED
                        pass
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
            
        
        
    