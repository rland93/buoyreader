from nose.tools import *
import buoyreader

def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")

def test_basic():
    print("I RAN!", end=' ')

def test_get_data():
    num = 22222
    buoyreader.get_buoy_data(num)