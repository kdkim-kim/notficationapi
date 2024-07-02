from app.config.db_controls import dataSearch, dataControl, create_table_if_not_exists

def userAPIkey(user:str, api_key:str): # 사용자의 보안키 비교
    str_sql = "select count(*) from login_pass where users = %s and a_key = %s"
    vars = [user, api_key]
    result = dataSearch(str_sql, vars)
    if result[0][0] == 0:
        return False
    else:
        return True

def create_tables(): # 테이블 생성
    create_table_if_not_exists()

def userPasschk(user:str, api_key:str): # 패스워드 유뮤 체크
    str_sql = "select pass_0 from login_pass where users = %s and a_key = %s"
    vals = [user, api_key]
    result = dataSearch(str_sql, vals)
    if result[0][0] == None or result[0][0] == "":
        return False
    else:
        return True

def cre_pass(user:str, api_key:str, pass0:str, pass1:str, pass2:str, pass3:str, pass4:str, pass5:str): # 패스워드 생성
    str_sql = "update login_pass set pass_0 = %s, pass_1 = %s, pass_2 = %s, pass_3 = %s, pass_4 = %s, pass_5 = %s where users = %s and a_key = %s"
    vars = [pass0, pass1, pass2, pass3, pass4, pass5, user, api_key]
    print(str_sql, vars)
    return dataControl(str_sql, vars)

def userPassAtuth(user:str, api_key:str): # 패스워드 검증
    str_sql = "select pass_0, pass_1, pass_2, pass_3, pass_4, pass_5 from login_pass where users = %s and a_key = %s"
    vars = [user, api_key]
    result = dataSearch(str_sql, vars)
    return result

def getSubclass(): #  분류값 추출
    str_sql = "select subclass from login_pass where users = %s and a_key = %s"
    vars = [user, api_key]
    result = dataSearch(str_sql, vars)
    return result