class Sql(object):
    def valid(self, sql):
        # select 语句必须包含条件where
        if sql.startswith("SELECT") or sql.startswith("select"):
            if 'where' not in sql and 'WHERE' not in sql:
                return "select 语句必须包含条件where", ""
        # delete 语句必须包含条件where
        elif sql.startswith("DELETE") or sql.startswith("delete"):
            if 'where' not in sql and 'WHERE' not in sql:
                return "delete 语句必须包含条件where", ""
        # sql 语句中尽量避免in操作
        elif " in " in sql:
            return "sql中不允许使用in操作", ""
        return None, sql


valid_sql = Sql()
