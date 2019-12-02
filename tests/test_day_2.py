import logging

import pytest

from day_2 import run_program

logging.getLogger().setLevel("DEBUG")


def test_1():
    assert run_program([1,0,0,0,99])[1] == [2,0,0,0,99]

def test_2():
    assert run_program([2,3,0,3,99])[1] == [2,3,0,6,99]

def test_3():
    assert run_program([2,4,4,5,99,0])[1] == [2,4,4,5,99,9801]

def test_4():
    assert run_program([1,1,1,4,99,5,6,0,99])[1] == [30,1,1,4,2,5,6,0,99]

def test_5():
    assert run_program([1,9,10,3,2,3,11,0,99,30,40,50])[1] == [3500,9,10,70,2,3,11,0,99,30,40,50]

