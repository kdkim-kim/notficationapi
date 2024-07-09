from datetime import datetime

from app.config.db_controls import dataSearch, dataControl, create_table_if_not_exists

class schema_auth: # 로그인 관련
    def __init__(self):
        pass

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


class schema_data: # 검색 관련
    def get_search_list(search_tag_0:int, search_tag_1:int, search_tag_2:int, search_tag_3:int, search_tag_4:int,
                        search_subClass:int, search_source:int): # SEARCH 버튼 클릭시 함수
        result = ((search_tag_0, search_tag_1, search_tag_2, search_tag_3, search_tag_4, search_subClass, search_source))
        return result

    def get_data_all(kind:str,varID:int): # 아이디로 모든 값 조회
        if kind =="content":
            str_sql = "select * from think_ where think_id = %s"
        elif kind == "class":
            str_sql = "select * from subClass where subClass_id = %s"
        elif kind == "source":
            str_sql = "select * from sources where source_id = %s"
        elif kind == "tags":
            str_sql = """
                select tags.tag From tags Inner Join tag_think On tag_think.tag_id = tags.tag_id
                where tag_think.think_id = %s
            """

        vars = [varID,]
        result = dataSearch(str_sql, vars)
        return result

    def get_data(kind, val): # 모든 값/ 특정한 값 반환 함 / 변수가 string
        if kind == "class":
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
        elif kind == "verify_source": # 삭제 전 점검
            str_sql = "select count(*) from think_ WHERE think_source = %s" # 내용에 소스가 있는지 점검
        if val:
            vars = [val,]
        else:
            vars = None

        result = dataSearch(str_sql, vars)
        print(result)
        return result

    def get_widget_tag(val:str): # 태그 위젯용 리스트
        str_sql = "select * FROM tags WHERE tag REGEXP %s ORDER BY tag"
        vars = [val,]
        return dataSearch(str_sql, vars)

class schema_in: # 입력 관련
################## 입력 메서드 ######################
    def in_sub_data(kind:str, val:str): # 분류 / 소스  등록
        if kind == "class":
            str_sql = "insert into subClass(subClass) values(%s)"
        elif kind == "source":
            str_sql = "insert into sources(source) values(%s)"
        elif kind == "tags":
            str_sql = "insert into tags(tag) values(%s)"
        vars = [val,]
        return dataControl(str_sql, vars)
    def in_think_tag(think_id:int, tag_id:int):
        str_sql = "insert into tag_think(think_id, tag_id) values(%s, %s)"
        vars = [think_id, tag_id]
        return dataControl(str_sql, vars)

    def in_thinks(title:str, contents:str, think_class:int, think_source:int, think_filePath:str, think_fileName:str): # 내용 입력
        str_sql = """
            insert into think_(title, contents, think_class, think_source, think_filePath, think_fileName, think_creDate, think_editDate) 
            values(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        vars = [title, contents, think_class, think_source, think_filePath, think_fileName, datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d')]
        return dataControl(str_sql, vars)

class schema_del:
################ 삭제 메서드 ######################
    def del_data_(kind, val): # 분류 / 소스  삭제
        if kind == "class":
            think_class_count = schema_data.get_data("verify_class", int(val))
            if think_class_count[0][0] > 0:
                return "unable"
            else:
                str_sql = "delete from subClass where subClass_id = %s"

        elif kind == "source":
            think_source_count = schema_data.get_data("verify_source", int(val))
            if think_source_count[0][0] > 0:
                return "unable"
            else:
                str_sql = "delete from sources where source_id = %s"

        vars = [val,]
        result = dataControl(str_sql, vars)
        if result:
            return "deleted"
        else:
            return "failed"

