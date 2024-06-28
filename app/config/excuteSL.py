from pymysql import connect
from app.config.db_controls import connect_db, dataSearch, dataControl

def userAPIkey(user:str, api_key:str):
    str_sql = "select count(*) from login_pass where users = %s and a_key = %s"
    vars = [user, api_key]
    result = dataSearch(str_sql, vars)
    if result[0][0] == 0:
        return False
    else:
        return True

def userPasschk(user:str, api_key:str):
    str_sql = "select pass_0 from login_pass where users = %s and a_key = %s"
    vals = [user, api_key]
    result = dataSearch(str_sql, vals)
    if result[0][0] == None or result[0][0] == "":
        return False
    else:
        return True

def cre_pass(user:str, api_key:str, pass0:str, pass1:str, pass2:str, pass3:str, pass4:str, pass5:str):
    str_sql = "update login_pass set pass_0 = %s, pass_1 = %s, pass_2 = %s, pass_3 = %s, pass_4 = %s, pass_5 = %s where users = %s and a_key = %s"
    vars = [pass0, pass1, pass2, pass3, pass4, pass5, user, api_key]
    print(str_sql, vars)
    return dataControl(str_sql, vars)