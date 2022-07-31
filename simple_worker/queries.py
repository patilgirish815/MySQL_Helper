def get_sp_list_for_db(databasename):
    return 'SELECT ROUTINE_NAME FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA = "'+ databasename +'"; '


def get_table_list_for_db(databasename):
    return 'SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = "' + databasename +'";'


def get_table_definition(tablename):
    return 'SHOW CREATE TABLE '+ tablename +';'


def get_sp_def_for_db_spname(databasename, spname):
    return 'SELECT ROUTINE_DEFINITION FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_SCHEMA = "' + databasename + '" AND ROUTINE_TYPE = "PROCEDURE" AND ROUTINE_NAME = "' + spname + '";'


def get_sp_def_for_db(databasename):
    return 'SELECT ROUTINE_NAME,ROUTINE_DEFINITION FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_SCHEMA = "' + databasename + '" AND ROUTINE_TYPE = "PROCEDURE";'


def get_sp_param_for_db_spname(databasename, spname):
    return 'SELECT PARAMETER_MODE, PARAMETER_NAME FROM information_schema.parameters WHERE SPECIFIC_SCHEMA = "' + databasename +'" AND SPECIFIC_NAME = "' + spname +'";'


def get_sp_param_for_db(databasename):
    return 'SELECT SPECIFIC_NAME, PARAMETER_MODE, PARAMETER_NAME FROM information_schema.parameters WHERE SPECIFIC_SCHEMA = "' + databasename +'";'


def get_index_list_for_db(databasename):
    return 'SELECT DISTINCT TABLE_NAME, COLUMN_NAME, INDEX_NAME FROM INFORMATION_SCHEMA.STATISTICS WHERE TABLE_SCHEMA = "' + databasename +'" ORDER BY INDEX_NAME;'


def get_fk_list_for_db(databasename):
    return 'SELECT TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = "' + databasename +'";'
