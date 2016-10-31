# -*- coding:utf-8 -*-

# 实现简单的缓存功能

import sqlite3
import datetime
import time


class Data(object):
    """
    数据存储结构
    """

    def __init__(self, r_key, r_val, r_expire_time):
        """
        :param r_key:
        :param r_val:
        :param r_expire_time: 将要过期的时间,精确到秒
        :return:
        """
        self.key = r_key
        self.val = r_val
        self.expire_time = r_expire_time


class PyCache(object):
    """
    # 实现简单的缓存功能
    """

    def __init__(self, r_store):
        """
        初始化
        :param r_store: 如果是字符串且后缀为.db则存储到sqlite,如果是字符串则存储到本地文件,如果是list则存储到内存
        :return:
        """
        if isinstance(r_store, str) and len(r_store) > 2 and r_store[-3:] == '.db':
            self.store_type = 'db'
        elif isinstance(r_store, str):
            self.store_type = 'file'
        elif isinstance(r_store, list):
            self.store_type = 'mem'
        else:
            raise 'StoreError', '存储方式设置错误'

        self.store = r_store
        if self.store_type == 'db':
            self.table = 't_' + self.store[:-3]
            self.db_conn = self._create_db()

    def set(self, r_key, r_val, r_expire=-1):
        """
        设置键值对
        :param r_key: 键
        :param r_val: 值
        :param r_expire:过期时间,如果过期时间为负值则持久存储
        :return:
        """
        if self.store_type == 'db':
            self._set_db_data(r_key, r_val, r_expire)

    def get(self, r_key):
        """
        获取键对应的值
        :param r_key:
        :return:
        """
        if self.store_type == 'db':
            return self._get_db_data(r_key)

    def _create_db(self):
        """
        创建db文件,及存储表
        :return:
        """
        conn = sqlite3.connect(self.store)
        cursor = conn.cursor()
        create_sql = 'create table if not exists %s (key varchar(64), val varchar(64), expire_time varchar(16))' % (
            self.table,)
        cursor.execute(create_sql)

        return conn

    def _set_db_data(self, r_key, r_val, r_expire):
        """
        :param r_key:
        :param r_val:
        :param r_expire:
        :return:
        """
        expire_time = self._get_expire_time(r_expire)
        cursor = self.db_conn.cursor()
        if self._is_key_exists(r_key):
            sql = "update {0} set val = '{1}', expire_time = '{2}' where key = '{3}' ".format(self.table, r_val,
                                                                                              expire_time, r_key)
        else:
            sql = "insert into {0} values ('{1}','{2}','{3}')".format(self.table, r_key, r_val, expire_time)
        print sql
        cursor.execute(sql)
        self.db_conn.commit()
        cursor.close()

    def _get_db_data(self, r_key):
        """
        :param r_key:
        :return:
        """
        if not self._is_key_exists(r_key):
            return
        sql = "select val,expire_time from %s where key = '%s' " % (self.table, r_key)
        cursor = self.db_conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        val = res[0]
        expire_time = int(res[1])
        if expire_time > self._get_expire_time(0):
            cursor.close()
            return val
        else:
            self._del_key(r_key)
            return

    def _del_key(self, r_key):
        """
        :param r_key:
        :return:
        """

        cursor = self.db_conn.cursor()
        del_sql = "delete from %s where key = '%s'" % (self.table, r_key)
        cursor.execute(del_sql)
        self.db_conn.commit()
        cursor.close()

    def _get_expire_time(self, r_expire):
        """
        :param r_expire:
        :return:
        """
        dela_secs = datetime.timedelta(seconds=r_expire)
        expire_time = datetime.datetime.now() + dela_secs

        return int(time.mktime(expire_time.timetuple()))

    def _is_key_exists(self, r_key):
        """
        :param r_key:
        :return:
        """
        sql = "select count(*) from %s where key = '%s' " % (self.table, r_key)
        cursor = self.db_conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        cursor.close()
        # print res
        return res[0]

    def ttl(self, r_key):
        """
        :param r_key:
        :return:
        """
        if not self._is_key_exists(r_key):
            return
        sql = "select val,expire_time from %s where key = '%s' " % (self.table, r_key)
        cursor = self.db_conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        expire_time = int(res[1])
        cursor.close()
        cur_time = self._get_expire_time(0)
        if expire_time > cur_time:
            return expire_time - cur_time
        else:
            self._del_key(r_key)
            return 0
