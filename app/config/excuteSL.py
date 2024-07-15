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

    def edit_passNum(user:str, api_key:str, pass0:str, pass1:str, pass2:str, pass3:str, pass4:str, pass5:str): # 패스워드 변경
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

        search_tags = [] # 검색된 태그 아이디 값
        if search_tag_0 != None:
            search_tags.append(search_tag_0)
        if search_tag_1 != None:
            search_tags.append(search_tag_1)
        if search_tag_2 != None:
            search_tags.append(search_tag_2)
        if search_tag_3 != None:
            search_tags.append(search_tag_3)
        if search_tag_4 != None:
            search_tags.append(search_tag_4)

        subVar = [] # SQL 입력 변수
        joinSQL = "" # 조인 sql
        whereSQL = "" # where sql
        class_source_in = bool # 분류나 소스 검색이 있는지 값
        print(search_subClass, search_source)
        if search_subClass == None and search_source == None:
            class_source_in = False
        else:
            if search_subClass != None and search_source == None:
                joinSQL = "Inner Join subClass On subClass.subClass_id = think_.think_class "
                whereSQL = "where think_.think_class = %s "
                subVar.append(search_subClass)
            elif search_subClass == None and search_source != None:
                joinSQL = "Inner Join sources On sources.source_id = think_.think_source "
                whereSQL = "where think_.think_source = %s "
                subVar.append(search_source)
            else: # 분류와 소스 모두 검색 할 때
                joinSQL = """
                    Inner Join subClass On subClass.subClass_id = think_.think_class 
                    Inner Join sources On sources.source_id = think_.think_source 
                    """
                whereSQL = "where think_.think_class = %s and think_.think_source = %s "
                subVar.append(search_subClass)
                subVar.append(search_source)
            class_source_in = True

        for i in range(len(search_tags)):
            if i == 0: # 검색 태그가 하나일 경우
                if class_source_in == True:
                    joinSQL = joinSQL + "Inner Join tag_think On tag_think.think_id = think_.think_id "
                    whereSQL = whereSQL + "and tag_think.tag_id = %s "
                else: # 분류와 출처가 없으면 WHERE 문구가 필요함
                    joinSQL = joinSQL + "Inner Join tag_think On tag_think.think_id = think_.think_id "
                    whereSQL = whereSQL + "where tag_think.tag_id = %s "
            else: # 검색 태그가 하나 이상일 경우
                joinSQL = joinSQL + f"Inner Join tag_think tag_think_{i} On tag_think_{i}.think_id = think_.think_id "
                whereSQL = whereSQL + f"and tag_think_{i}.tag_id = %s "

            subVar.append(search_tags[i])    # 변수값 저장

        str_sql = """
            select DISTINCT think_.think_id, think_.title, think_.think_class, think_.think_source,
            think_.think_fileName, think_.think_editDate from think_
        """
        str_sql = f"{str_sql} {joinSQL} {whereSQL} order by think_.think_editDate desc LIMIT 30"
        print(str_sql, subVar)
        result = dataSearch(str_sql, subVar)
        #result = ((search_tag_0, search_tag_1, search_tag_2, search_tag_3, search_tag_4, search_subClass, search_source))
        return result

    def get_data_all(kind:str,varID:int): # 아이디로 모든 값 조회
        if kind =="content":
            str_sql = "select * from think_ where think_id = %s"
        elif kind == "class":
            str_sql = "select * from subclass where subClass_id = %s"
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
        elif kind == "tags_null": # 연결없는 빈태그 검색
            str_sql = "select tags.tag_id From tags Left Join tag_think On tag_think.tag_id = tags.tag_id "
            str_sql = str_sql + "Where tag_think.think_id Is Null"
            print(str_sql)
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

################ 업데이트 메서드 ###################
    def update_thinks(think_id:int, title:str, contents:str, think_class:int, think_source:int, think_filePath:str, think_fileName:str): # 내용 수정
        str_sql = """
            update think_ set title = %s, contents = %s, think_class = %s, think_source = %s, think_filePath = %s, think_fileName = %s, think_editDate = %s
            where think_id = %s
        """
        vars = [title, contents, think_class, think_source, think_filePath, think_fileName, datetime.now().strftime('%Y-%m-%d'), think_id]
        print(str)
        result = dataControl(str_sql, vars)
        print(result)
        return result
class schema_del:
################ 삭제 메서드 ######################
    def del_data_(kind, val): # 분류 / 소스  삭제
        print(kind, val)
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
        elif kind == "content":
            str_sql = "delete from think_ where think_id = %s"

        elif kind == "tags_think":
            str_sql = "delete from tag_think where think_id = %s"
        elif kind == "tags":
            str_sql = "delete from tags where tag_id = %s"

        vars = [val,]
        result = dataControl(str_sql, vars)
        if result:
            return "deleted"
        else:
            return "failed"

