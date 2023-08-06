from authc.core import gunload
import pymysql
from typing import Tuple


class MyRedisBySQL(object):
    """ A redis server implemented with SQL
    columns: (rkey, rvalue)
    """

    def __init__(self, tablename: str = 'redis') -> None:
        self._client = None
        self.tablename = tablename

    @property
    def client(self):
        if self._client is None:
            account = gunload('mysql')
            host, user, passwd = account.split('/')
            self.db = pymysql.connect(host=host, user=user,
                                      password=passwd, db=user)
            self._client = self.db.cursor()
        return self._client

    def get(self, key: str) -> Tuple[str, str]:
        cmd = f'SELECT rvalue FROM {self.tablename} WHERE rkey = "{key}";'
        self.client.execute(cmd)
        res = self.client.fetchall()
        if not res:
            return None
        return res[0][0]

    def set(self, key: str, value: str) -> bool:
        assert len(value) < 10240, "maximum length of value is 10240"
        cmd = f'INSERT INTO {self.tablename} values ("{key}", "{value}")\
         ON DUPLICATE KEY UPDATE rvalue = "{value}";'
        self.client.execute(cmd)
        self.db.commit()
        return True

    def delete(self, key: str) -> bool:
        cmd = f'DELETE FROM {self.tablename} WHERE rkey = "{key}";'
        self.client.execute(cmd)
        self.db.commit()
        return True


def easysql():
    return MyRedisBySQL()
