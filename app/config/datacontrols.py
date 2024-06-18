import pymysql
from app.config.db_con import get_connection

def dataControl(strsql, inVal):  # 데이타 입력 수정 삭제 컨트롤 함수
     mydb = get_connection()
     cursor = mydb.cursor()
     try:
         cursor.execute(strsql, inVal)
         mydb.commit()
         last_id = 0

         if "insert" in strsql:
             last_id = cursor.lastrowid
         elif "update" in strsql or "delete" in strsql:
             last_id = inVal
         cursor.close()
         return last_id
     except pymysql.Error as err:
         print(f"Error: {err}, sql: {strsql}, inVal: {inVal}")
     finally:
         mydb.close()

def dataSearch(sql, inVal):  # 데이타 검색 컨트롤 함수
    mydb = get_connection()
    cursor = mydb.cursor()
    try:
        cursor.execute(sql, inVal)
        result = cursor.fetchall()
        cursor.close()
        return result
    except pymysql.Error as err:
        print(f"Error: {err} , sql: {sql}, inVal: {inVal}")
    finally:
        mydb.close()

