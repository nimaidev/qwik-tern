from qwik_tern.logger.logger import setup_logger


PRE_CONDITION = ["SELECT", "COUNT"]

logger = setup_logger(__name__)

class SQLValidator:

    def validate_pre_condition(self, sql_q: str):
        # logger.debug(sql_q)
        if isinstance(sql_q, tuple):
            sql_q = sql_q[0] if sql_q else ''  # Take the first item if it's a non-empty tuple
    
        if not isinstance(sql_q, str):
            raise TypeError(f'Expected SQL string but got {type(sql_q).__name__}')
        
        normalized_sql = sql_q.strip().upper()
        if not any(normalized_sql.startswith(pre) for pre in PRE_CONDITION):
            raise Exception(f'Invalid PRE condition [{sql_q}]')
    
    def validate_rollback_cmd(self, sql_q: str) -> bool:
        return True
