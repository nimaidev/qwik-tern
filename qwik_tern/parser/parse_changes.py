

import sys
from qwik_tern.logger.logger import setup_logger
from qwik_tern.models.changelog_model import DBChangelogModel
from qwik_tern.validator.sql_validator import SQLValidator

logger = setup_logger(__name__)

class ChangesParser:
    def __init__(self, db_changes : DBChangelogModel):
        self.db_changes = db_changes
    
    
    def validate(self) -> bool:
        try:     
            sql_validator = SQLValidator()
            if self.db_changes.pre is not None or self.db_changes.pre != "":
                raise sql_validator.validate_pre_condition(self.db_changes.pre)
            
            if self.db_changes.rollback is not None or self.db_changes.rollback != "":
                return sql_validator.validate_pre_condition(self.db_changes.rollback)
            
            
        except Exception as e:
            logger.critical(f"Exception : {e} ")
            sys.exit(0)