# -*- coding: utf-8 -*-
"""
@file: adapter.py
@desc:
@author: Jaden Wu
@time: 2021/10/1 20:41
"""


class Monitor(object):
    """
    直接接入系统的设备
    """
    def __init__(self, code, init_state):
        self.code = code
        self.init_state = init_state
        self.last_state = None
        self.current_state = None
        self.is_connect = True

    def set_state(self, new_state):
        """
        设置控制器的状态
        :param new_state:
        :return:
        """
        self.last_state = self.current_state
        self.current_state = new_state

    def reset(self):
        """
        复位
        :return:
        """
        self.last_state = self.init_state
        self.current_state = self.init_state
