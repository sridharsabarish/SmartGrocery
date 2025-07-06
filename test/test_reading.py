import sys
import os


import pandas as pd



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from Visuals import Visuals
from loguru import logger
from Reading import Reading

class TestReading:
    
    def test_create_reader_objects(self):
        try:
            
            reader = Reading();
            assert True
        except:
            assert False
        