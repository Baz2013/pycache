# -*- coding:utf-8 -*-

# 实现简单的缓存功能

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

    def set(self, r_kv, r_expire=-1):
        """
        设置键值对
        :param r_kv: 键值对
        :param r_expire:过期时间,如果过期时间为负值则持久存储
        :return:
        """

    def get(self, r_key):
        """
        获取键对应的值
        :param r_key:
        :return:
        """
