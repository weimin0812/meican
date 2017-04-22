# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from enum import Enum


class TabStatus(Enum):
    AVAIL = 'AVAILABLE'
    CLOSED = 'CLOSED'
    NOT_YET = 'NOT_YET'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def parse(cls, string_value):
        """
        :type string_value: str | unicode
        :rtype: TabStatus
        """
        value_enums = {
            'AVAILABLE': cls.AVAIL,
            'CLOSED': cls.CLOSED,
        }
        return value_enums.get(string_value, cls.UNKNOWN)


class ReadableObject(object):
    """
    just define __unicode__ to make a object readable
    """

    def __unicode__(self):
        return '<{}>'.format(self.__class__)

    def __repr__(self):
        return self.__unicode__().encode('utf-8')


class Address(ReadableObject):
    """
    地址
    """

    def __init__(self, data):
        """
        :type data: dict
        """
        self.uid = data['uniqueId']
        self.address = data['address']  # 公司地址
        self.pick_up = data['pickUpLocation']  # 取餐地址

    def __unicode__(self):
        return '{} {}'.format(self.uid, self.address)


class Tab(ReadableObject):
    """
    一个 Tab 代表一个时间窗口
    比如 中饭点餐时间
    或者 晚饭点餐时间
    """

    def __init__(self, data):
        """
        :type data: dict
        """
        self.title = data['title']
        self.target_time = datetime.fromtimestamp(int(data['targetTime']) / 1000)
        self.status = TabStatus.parse(data['status'])
        self.uid = data['userTab']['uniqueId']
        self.addresses = [_ for _ in data['userTab']['corp']['addressList']]

    def __unicode__(self):
        return '{} {} {}'.format(self.status.value, self.target_time.strftime('%Y-%m-%d'), self.title)
