import pymysql

def get_connection():
    conn = pymysql.connect(
        host="localhost",
        user="peNoteUser",
        password="99Note8877",
        db="thoughtNote",
        port=3306,
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn