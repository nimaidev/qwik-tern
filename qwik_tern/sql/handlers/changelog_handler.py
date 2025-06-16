
import hashlib
from qwik_tern.logger.logger import setup_logger
from qwik_tern.models.changelog_model import DBChangelogModel
from qwik_tern.sql.helpers.mysql_helper import MySQLHelper

logger = setup_logger(__name__)
class ChangelogHandler:
        
    def check_if_executed(self, changelog : DBChangelogModel) -> bool:
        query = f"""
            SELECT COUNT(*) 
            FROM TERNCHANGELOGS 
            WHERE ID = '{changelog.key}' 
            AND AUTHOR = '{changelog.author}'
        """
        mySqlHelper = MySQLHelper()
        count = mySqlHelper.execute_count(query)
        if count > 0:
            return True
        else:
            return False
    
    def checksum_check(self, checksum_old : str, changelog : DBChangelogModel):
        # TODO: check for checksum 
        pass
    
    def calculate_checksum(self, changelog: DBChangelogModel):
        hash_lib = hashlib.sha256()
        changes_str = str(changelog.changes)
        changes_bytes = changes_str.encode('utf-8')
        hash_lib.update(changes_bytes)
        logger.info(hash_lib.hexdigest())
        return hash_lib.hexdigest()