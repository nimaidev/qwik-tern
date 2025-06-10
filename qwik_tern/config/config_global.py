import os
import sys

from qwik_tern.logger.logger import setup_logger
import configparser

from qwik_tern.models.global_config_model import GlobalConfigModel
from qwik_tern.thread_local import Current

logger = setup_logger(__name__)

class GlobalConfig:
    
    @staticmethod
    def initialize():
        config_file =  GlobalConfig().__check_for_config_file()
        GlobalConfig().__read_config(config_file)
        
    def __check_for_config_file(self):
        # Check for .tern.ini file in the project root
        project_root = os.path.abspath(os.path.dirname(__file__))
        while project_root and not os.path.isfile(os.path.join(project_root, '.tern.ini')):
            parent = os.path.dirname(project_root)
            if parent == project_root:  # Reached filesystem root
                project_root = None
            else:
                project_root = parent
        
        if project_root:
            config_path = os.path.join(project_root, '.tern.ini')
            logger.info(f"Root folder found : {config_path}")
            return config_path
        else:
            logger.critical("Qwik tern configuration not found.")
            sys.exit(0)
            return None  
        
    def __read_config(self, config_file_path : str):
            config = configparser.ConfigParser()
            try:
                config.read(config_file_path)
                
                if 'global' in config:
                    global_section = config['global']
                    logger.info(f"Global configuration loaded from {config_file_path}")
                    # Get the root directory (remove the .tern.ini file from path)
                    root_dir = os.path.dirname(config_file_path)
                    changelog_dir = global_section.get('changelog_dir')
                    # Remove quotes if present in changelog_dir
                    if changelog_dir and (changelog_dir.startswith('"') and changelog_dir.endswith('"')) or \
                                        (changelog_dir.startswith("'") and changelog_dir.endswith("'")):
                        changelog_dir = changelog_dir[1:-1]
                    global_config_model = GlobalConfigModel(
                        root_dir=root_dir,
                        changelog_dir=changelog_dir,
                        log_level=global_section.get('log_level')
                    )
                    logger.info(f"Config: {global_config_model.changelog_dir}")
                    Current.setConfig(globalConfigModel=global_config_model)
                else:
                    logger.warning(f"No [global] section found in {config_file_path}")
                    sys.exit(0)
            except Exception as e:
                logger.error(f"Error reading configuration file {config_file_path}: {str(e)}")
                sys.exit(0)        