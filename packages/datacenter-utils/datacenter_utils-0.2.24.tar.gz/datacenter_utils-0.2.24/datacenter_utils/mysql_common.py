import pymysql
import pandas as pd


# ---- 用pymysql 操作数据库
def get_connection(db, user, password, host='127.0.0.1', port=3306):
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn


# ---- 使用 with 的方式来优化代码
class Mysql(object):

    def __init__(self, commit=True):
        """

        :param commit: 是否在最后提交事务(设置为False的时候方便单元测试)
        """
        self._commit = commit

    def __enter__(self):
        # 在进入的时候自动获取连接和cursor
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False

        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, *exc_info):
        # 提交事务
        if self._commit:
            self._conn.commit()
        # 在退出的时候自动关闭连接和cursor
        self._cursor.close()
        self._conn.close()

    @property
    def cursor(self):
        return self._cursor


if __name__ == '__main__':
    with Mysql() as my:
        my.cursor.execute("select * from der_focus_sw")
        data = my.cursor.fetchall()
    df = pd.DataFrame(data)
