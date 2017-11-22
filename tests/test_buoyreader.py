from nose.tools import *
from buoyreader import buoyreader

def setup():
    print("SETUP")

def teardown():
    print("TEAR DOWN")

def test_basic():
    print("I RAN!", end=' ')

def test_bad_buoy_number():
    # bad buoy number 22222
    buoy_number = 99999
    assert buoyreader.get_buoy_data(buoy_number) = Exception