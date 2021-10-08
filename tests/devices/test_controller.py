# -*- coding: utf-8 -*-
"""
@file: test_controller.py
@desc:
@author: Jaden Wu
@time: 2021/10/1 20:51
"""
from devices.controller import Controller


def test_controller():
    d = Controller(code="01", init_state=0)
    d.set_state(1)
    d.set_state(2)
    assert d.current_state == 2
    assert d.last_state == 1
    d.reset()
    assert d.current_state == 0
    assert d.last_state == 0
