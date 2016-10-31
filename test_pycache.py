# -*- coding:utf-8 -*-

import unittest
from pycache import *
import time


class CacheTest(unittest.TestCase):
    def setUp(self):
        self.ins = PyCache('cache.db')

    def test_set(self):
        """
        :return:
        """
        self.ins.set('name', 'gucb', 20)
        self.ins.set('name1', 'liu', 60 * 10)

    def test_get_expire_time(self):
        self.assertEquals(self.ins._get_expire_time(20), self.ins._get_expire_time(0) + 20)

    def test_get(self):
        print self.ins.get('name')

    def test_ttl(self):
        self.ins.set('name2', 'lllll', 10)
        time.sleep(10)
        self.assertEquals(0, self.ins.ttl('name2'))

    def test_ttl_1(self):
        self.ins.set('name3', 'ssss', 20)
        time.sleep(5)
        self.assertEquals(15, self.ins.ttl('name3'))
