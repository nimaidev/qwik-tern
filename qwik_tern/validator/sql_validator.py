

class SQLValidator:
    def validate_pre_condition(self, sql_q : str) -> Exception:
        raise Exception(f'Invalid PRE condition : {sql_q}')
        return True
    
    
    def validate_rollback_cmd(self, sql_q : str) -> bool:
        return True