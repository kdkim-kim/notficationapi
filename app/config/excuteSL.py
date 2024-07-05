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

def get_data(kind, val): # 모든 값/ 특정한 값 반환 함
    if kind == "class":
        print(val)
        if val == None:
            str_sql = "select * from subClass ORDER BY subClass"
        else:
            str_sql = "select * from subClass WHERE subClass = %s"
    elif kind == "source":
        if val == None:
            str_sql = "select * from sources ORDER BY source"
        else:
            str_sql = "select * from sources WHERE source = %s"
    elif kind == "tags":
        if val == None:
            str_sql = "select * from tags ORDER BY tag"
        else:
            str_sql = "select * from tags WHERE tag = %s"
    elif kind == "verify_class": # 삭제 전 점검
        str_sql = "select count(*) from think_ WHERE think_class = %s" # 내용에 분류가 있는지 점검
    if val:
        vars = [val,]
    else:
        vars = None
    result = dataSearch(str_sql, vars)
    return result

def get_widget_tag(val:str): # 태그 위젯용 리스트
    str_sql = "select * FROM tags WHERE tag REGEXP %s ORDER BY tag"
    vars = [val,]
    return dataSearch(str_sql, vars)

################## 입력 메서드 ######################
def in_sub_data(kind, val): # 분류 / 소스  등록
    if kind == "class":
        str_sql = "insert into subClass(subClass) values(%s)"
    elif kind == "source":
        str_sql = "insert into sources(source) values(%s)"
    vars = [val,]
    return dataControl(str_sql, vars)

################ 삭제 메서드 ######################
def del_data_(kind, val): # 분류 / 소스  삭제
    print("delete method called")
    if kind == "class":
        think_class_count = get_data("verify_class", val)
        if think_class_count[0][0] > 0:
            return "unable"
        else:
            str_sql = "delete from subClass where subClass_id = %s"

    elif kind == "source":
        str_sql = "delete from sources where source_id = %s"
    vars = [val,]
    result = dataControl(str_sql, vars)
    print(result)
    if result:
        return "deleted"
    else:
        return "failed"

