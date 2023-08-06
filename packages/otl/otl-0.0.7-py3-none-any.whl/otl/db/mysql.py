# -*- coding: utf-8 -*-
import pymysql
from dbutils.pooled_db import PooledDB
from otl.db.common.SQL import valid_sql


class MysqlDbBase:
    host = None
    port = 3306
    user = None
    password = None
    db = None
    __pool = None

    def __init__(self):
        self.pool = self.__get_conn_pool()

    def __get_conn_pool(self):
        if not self.__pool:
            try:
                self.__pool = PooledDB(
                    creator=pymysql,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    db=self.db
                )
            except Exception as err:
                raise Exception("Error: connect mysql error %s", err)
        return self.__pool

    def _get_connection(self):
        conn = self.pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cursor

    def _close_connection(self, conn, cursor):
        if conn:
            conn.close()
        if cursor:
            cursor.close()

    def queryone(self, sql, params=()) -> dict:
        """
        单条数据查询
        :param sql:
        :param params:
        :return: result dict
        """
        conn, cur = self._get_connection()
        try:
            err, v_sql = valid_sql.valid(sql)
            if err:
                raise Exception("sql valid Error: %s", err)
            row = cur.execute(v_sql, params)
            if row == 0:
                return {}
            else:
                return cur.fetchone()
        except Exception as err:
            raise Exception(f"Query Error: {err} = {sql}")
        finally:
            self._close_connection(conn, cur)

    def query(self, sql, params=()) -> list:
        """
        查询方法
        :param params:
        :param sql:
        :return: result List
        """
        conn, cur = self._get_connection()
        try:
            result = []
            # 校验sql合规
            err, v_sql = valid_sql.valid(sql)
            if err is not None:
                raise Exception(err)

            row = cur.execute(v_sql, params)
            if row == 0:
                return result
            else:
                for rest in cur.fetchall():
                    result.append(rest)
                return result
        except Exception as err:
            raise Exception(f"Query Error: {err} - {sql}")
        finally:
            self._close_connection(conn, cur)

    def insert(self, sql, params=()) -> int:
        """
        插入方法
        :param params:
        :param sql:
        :return:
        """
        return self._update("Insert", sql, params)

    def update(self, sql, params=()) -> int:
        """
        更新方法
        :param params:
        :param sql:
        :return:
        """
        return self._update("Update", sql, params)

    def delete(self, sql, params=()) -> int:
        """
        删除方法
        :param params:
        :param sql:
        :return:
        """
        self._update("Delete", sql, params)

    def _update(self, modify_type, sql, params=()) -> int:
        conn, cur = self._get_connection()
        try:
            # 校验sql合规
            err, v_sql = valid_sql.valid(sql)
            if err is not None:
                raise Exception(err)
            rows = cur.execute(v_sql, params)
            conn.commit()
            return rows
        except Exception as err:
            raise Exception(f"{modify_type} Error: {err} - {sql}")
        finally:
            self._close_connection(conn, cur)
