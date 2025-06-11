

import sys
from qwik_tern.logger.logger import setup_logger
from qwik_tern.models.changelog_model import DBChangelogModel
from qwik_tern.validator.sql_validator import SQLValidator
from sql.handlers.command_handler import ChangelogCommandHandler

logger = setup_logger(__name__)

class ChangesParser:
    def __init__(self, db_changes : DBChangelogModel):
        self.db_changes = db_changes
    
    
    def validate(self) -> bool:
        try:     
            sql_validator = SQLValidator()
            # logger.debug(self.db_changes.pre)
            if self.db_changes.pre is not None :
                if isinstance(self.db_changes.pre, str) and self.db_changes.pre != "":
                    sql_validator.validate_pre_condition(self.db_changes.pre)
                    # TODO: Need to add later
                else:
                    raise Exception(f"Invalid PRE condition: {self.db_changes.pre}")
            
            if self.db_changes.rollback is not None and self.db_changes.rollback != "":
                # TODO: Need to add later
                return sql_validator.validate_pre_condition(self.db_changes.rollback)
            
            
            if self.db_changes.changes is not None:
                changelogCommandHandler = ChangelogCommandHandler()
                changelogCommandHandler.handle(self.db_changes.changes)
            else:
                raise Exception("Atleast one changelog required for changelog execution")
            
            
        except Exception as e:
            
            logger.critical(f"Exception : {e}")
            sys.exit(0)