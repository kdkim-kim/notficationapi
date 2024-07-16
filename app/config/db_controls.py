import os, json
from pymysql import connect

file_jason = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secrets.json") # 디비 접속 자료 json 파일
secrets_data = json.loads(open(file_jason).read())
db = secrets_data["DB"]
db_host = db["Host"]
db_user = db["User"]
db_passwd = db["Password"]
db_database = db["Database"]

cre_tables=["think_","tags","subclass","sources","login_pass","tag_think"] #DB 테이블 이름

def connect_db():  #DB 접속 함수
    print(db_host, db_user, db_passwd, db_database)
    try:
        mydb = connect(
            host=db_host, user=db_user, passwd=db_passwd, database=db_database
        )
        return mydb
    except connect.Error as err:
        print(err)
        return None
def create_table_if_not_exists():   #테이블이 없을시 생성
    mydb = connect_db()
    cursor = mydb.cursor()
    cursor.execute("Show tables")
    tables = cursor.fetchall()
    cursor.close()
    mydb.close()

    count = len(cre_tables)     #테이블 이름에서 얻은 갯수 값
    for i in range(count):
        if cre_tables[i] not in str(tables): #테이블명이 없을시 생성
            create_tables(cre_tables[i]) # 테이블 생성 함수

def create_tables(var): #DB_ 테이블 생성
    table_sql = ""
    if var == "think_":
        table_sql = """
            CREATE TABLE `think_` (
	        `think_id` INT(11) NOT NULL AUTO_INCREMENT,
	        `title` VARCHAR(100) NOT NULL DEFAULT '0' COLLATE 'utf8mb4_general_ci',
	        `contents` MEDIUMTEXT NOT NULL,
	        `think_class` INT(11) NOT NULL,
	        `think_source` INT(11) NULL DEFAULT NULL,
	        `think_filePath` CHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	        `think_fileName` CHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	        `think_creDate` DATE NOT NULL,
	        `think_editDate` DATE NOT NULL DEFAULT curdate(),
	        PRIMARY KEY (`think_id`) USING BTREE
            )
            COLLATE='utf8mb4_general_ci'
            ENGINE=InnoDB;
        """
    elif var == "tags":
        table_sql = """
            CREATE TABLE `tags` (
	        `tag_id` INT(11) NOT NULL AUTO_INCREMENT,
	        `tag` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	        PRIMARY KEY (`tag_id`) USING BTREE
            ) COLLATE='utf8mb4_general_ci' ENGINE=InnoDB;
        """
    elif var == "subclass":
        table_sql = """
            CREATE TABLE `subClass` (
	        `subClass_id` INT(11) NOT NULL AUTO_INCREMENT,
	        `subClass` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	        PRIMARY KEY (`subClass_id`) USING BTREE
            ) COLLATE='utf8mb4_general_ci' ENGINE=InnoDB;
        """
    elif var == "sources":
        table_sql = """
            CREATE TABLE `sources` (
	        `source_id` INT(11) NOT NULL AUTO_INCREMENT,
	        `source` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	        PRIMARY KEY (`source_id`) USING BTREE
            ) COLLATE='utf8mb4_general_ci' ENGINE=InnoDB;
        """
    elif var == "tag_think":
        table_sql = """
            CREATE TABLE `tag_think` (
	        `tag_id` INT NOT NULL,
	        `think_id` INT NOT NULL,
	        CONSTRAINT `FK__think_` FOREIGN KEY (`think_id`) REFERENCES `think_` (`think_id`) ON UPDATE NO ACTION ON DELETE CASCADE,
	        CONSTRAINT `FK__tags` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`) ON UPDATE NO ACTION ON DELETE NO ACTION
            ) COLLATE='utf8mb4_general_ci' ;
        """
    if table_sql:
        mydb = connect_db()
        cursor = mydb.cursor()
        try:
            cursor.execute(table_sql)
            mydb.commit()
        except connect.Error as err:
            print(f"Error: {err}, sql: {table_sql}")
        finally:
            cursor.close()
            mydb.close()

def dataControl(strsql, inVal):    # 데이타 입력 수정 삭제 컨트롤 함수
    mydb = connect_db()
    cursor = mydb.cursor()
    try:
        cursor.execute(strsql, inVal)
        mydb.commit()
        last_id = 0

        if "insert" in strsql :
            last_id = cursor.lastrowid
        elif "update" in strsql or "delete" in strsql:
            last_id = inVal
        cursor.close()
        #print(strsql, inVal, last_id)
        return last_id
    except connect.Error as err:
        print(f"Error: {err}, sql: {strsql}, inVal: {inVal}")
    finally:
        mydb.close()


def dataSearch(sql, inVal):   # 데이타 검색 컨트롤 함수
    mydb = connect_db()
    cursor = mydb.cursor()
    try:
        cursor.execute(sql, inVal)
        result = cursor.fetchall()
        cursor.close()
        return result
    except connect.Error as err:
        print(f"Error: {err} , sql: {sql}, inVal: {inVal}")
    finally:
        mydb.close()

