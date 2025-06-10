
class DbConfig:
    def __init__(self, host: str, port : int, user :str, passw :str, db: str):
        self.host = host
        self.port = port
        self.user = user
        self.passw = passw
        self.db = db