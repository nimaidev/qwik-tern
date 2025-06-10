

import json
import os
import sys
from qwik_tern.logger.logger import setup_logger
from qwik_tern.models.changelog_model import DBChangelogModel
from qwik_tern.parser.parse_changes import ChangesParser
from qwik_tern.thread_local import Current

logger = setup_logger(__name__)


class ParseFiles:
    
    def __init__(self):
        self.root_dir = Current.getConfig().root_dir
        self.changelog_dir = Current.getConfig().changelog_dir 
    
    def process_changelog_files(self):
        try:
            current_dir = os.path.join(self.root_dir, self.changelog_dir)
            for root, dirs, files in os.walk(current_dir):
                for file in files:
                    # file_path = os.path.join(root, file)
                    if file.endswith(".json"):
                        logger.info(f"Processing file: {file}")
                        self.parse_json_file(os.path.join(current_dir, file))
                    else:
                        logger.warning(f"skipping non-json files: {file}")
        except Exception as e:
            logger.critical(f"Unable to process changelog documents: {e}")
            sys.exit(0)
    
    def parse_json_file(self, file :str):
        try:
            with open(file, 'r', encoding="UTF-8") as file_json:
                json_data = json.load(file_json)
                
                database_changes = json_data["databaseChanges"]
                if database_changes is None:
                    logger.critical("INVALID changelog file!!!")
                    sys.exit(0)
                logger.info(f"json data {len(database_changes)}")
                for change_set in database_changes:
                    logger.info(f"changeset : {change_set}")
                    self.validate_changes(change_set)
                    
        except Exception as e:
            if isinstance(e, KeyError):
                logger.critical(f"Invalid Key: {e}")
            else:
                logger.critical(f"Invalid database changelog {e}")
            sys.exit(0)

    
    def validate_changes(self, changelog : json):
        try:            
            changelog= changelog.get("changeSet")
            changelog_model = DBChangelogModel(
                key= changelog.get("key"),
                author=changelog.get("author"),
                changes= changelog.get("changes"),
                pre = changelog.get("pre"),
                rollback=changelog.get("rollback"),
                comment=changelog.get("comment")
            )
            logger.info(changelog_model.key)
            change_parser = ChangesParser(changelog_model)
            change_parser.validate()
        except Exception as e:
            if isinstance(e, KeyError):
                logger.critical(f"Invalid Key: {e}")
            else:
                logger.critical(f"Invalid database changelog {e}")
            sys.exit(0)
                