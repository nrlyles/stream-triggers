#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from stream_trigger.bulb.base import BaseBulb

__author__ = "nlyles"
__copyright__ = "nlyles"
__license__ = "none"



@pytest.fixture()
def bulb():
    return BaseBulb()


def test_instantiate(bulb):
    test_bulb = bulb


def test_set_off(bulb):
    with pytest.raises(NotImplementedError):
        bulb.set_off()


def test_set_on(bulb):
    with pytest.raises(NotImplementedError):
        bulb.set_on()

def test_set_color(bulb):
    with pytest.raises(NotImplementedError):
        bulb.set_color("771d1d")