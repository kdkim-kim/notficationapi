from app.config.datacontrols import dataSearch
class DB_source:
    def __init__(self, queryVal: list ):
        self.queryList = queryVal

    def chk_password(self):
        mode = self.queryList[0]
        if mode == "count":
            strSQL = "SELECT COUNT(*) FROM login_pass;"
            inVar = None
            result = dataSearch(strSQL, inVar)
            if result[0]["COUNT(*)"] > 0:
                return False
            else:
                return True
        elif mode == "check":
            strSQL = """
                select count(*) FROM login_pass WHERE pass_0 = %s and pass_1 = %s
                and pass_2 = %s and pass_3 = %s and pass_4 = %s and pass_5 = %s
            """
            del self.queryList[0]
            inVar = self.queryList
            result = dataSearch(strSQL, inVar)
            if result[0]["COUNT(*)"] == 0:
                return False
            else:
                return True




