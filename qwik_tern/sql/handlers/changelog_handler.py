
from qwik_tern.logger.logger import setup_logger
from qwik_tern.models.changelog_model import DBChangelogModel
from qwik_tern.sql.helpers.mysql_helper import MySQLHelper

logger = setup_logger(__name__)
class ChangelogHandler:
        
    def check_if_executed(self, changelog : DBChangelogModel) -> bool:
        query = f"""
            SELECT COUNT(*) 
            FROM TERNCHANGELOGS 
            WHERE ID = {changelog.key} 
            AND AUTHOR = {changelog.author}
        """
        mySqlHelper = MySQLHelper()
        count = mySqlHelper.execute_count(query)
        if count > 0:
            return True
        else:
            return False
    
    def checksum_check(self, changelog : DBChangelogModel):
        # TODO: check for checksum 
        pass