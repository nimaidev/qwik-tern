

import os
import sys
from qwik_tern.logger.logger import setup_logger
from qwik_tern.thread_local import Current

logger = setup_logger(__name__)


class ParseFiles:
    
    def __init__(self):
        self.root_dir = Current.getConfig().root_dir
        self.changelog_dir = Current.getConfig().changelog_dir 
    
    def process_changelog_files(self):
        try:
            logger.info(os.path.join(self.root_dir, self.changelog_dir))
            for root, dirs, files in os.walk(os.path.join(self.root_dir, self.changelog_dir)):
                for file in files:
                    # file_path = os.path.join(root, file)
                    if file.endswith(".json"):
                        logger.info(f"Processing file: {file}")
                    else:
                        logger.warning(f"skiping non-json files: {file}")
        except Exception as e:
            logger.critical(f"Unable to process changelog documents: {e}")
            sys.exit(0)