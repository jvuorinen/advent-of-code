import pytest

from day_2 import compute

def test_1():
    assert compute([1,0,0,0,99]) == [2,0,0,0,99]

def test_2():
    assert compute([2,3,0,3,99]) == [2,3,0,6,99]

def test_3():
    assert compute([2,4,4,5,99,0]) == [2,4,4,5,99,9801]

def test_4():
    assert compute([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

def test_5():
    assert compute([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]

