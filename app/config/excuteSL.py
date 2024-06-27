from pymysql import connect
from app.config.db_controls import connect_db, dataSearch, dataControl

def userAPIkey(user:str, api_key:str):
    str_sql = "select count(*) from login_pass where users = %s and a_key = %s"
    val = [user, api_key]
    result = dataSearch(str_sql, val)
    if result[0][0] == 0:
        return False
    else:
        return True