

class GlobalConfigModel:
    def __init__(self, root_dir: str, changelog_dir : str, log_level : str):
        self.root_dir = root_dir
        self.changelog_dir = changelog_dir
        self.log_level = log_level