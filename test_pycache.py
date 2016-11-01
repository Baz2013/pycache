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
        self.ins.set('foo', 'bar', 10)
        self.assertEquals('bar', self.ins.get('foo'))

    def test_get_1(self):
        self.ins.set('foo1', 'bar', 2)
        time.sleep(2)
        self.assertEquals(None, self.ins.get('foo1'))

    def test_ttl(self):
        self.ins.set('name2', 'lllll', 10)
        time.sleep(10)
        self.assertEquals(0, self.ins.ttl('name2'))

    def test_ttl_1(self):
        self.ins.set('name3', 'ssss', 20)
        time.sleep(5)
        self.assertEquals(15, self.ins.ttl('name3'))

    def test_set_1(self):
        s = time.clock()
        for i in range(10):
            name = 'name%03d' % (i,)
            self.ins.set(name, 'ooooooooooo', 20)
        print 'time: ', time.clock() - s

    def test_ttl_2(self):
        for i in range(10):
            name = 'name%03d' % (i,)
            print self.ins.ttl(name)
