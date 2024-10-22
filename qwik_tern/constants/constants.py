

CHECK_IF_TABLE_EXISTS = """ SELECT COUNT(*) 
    FROM information_schema.tables 
    WHERE table_schema = 'ai-service' 
    AND table_name = 'db_changelog' 
    """