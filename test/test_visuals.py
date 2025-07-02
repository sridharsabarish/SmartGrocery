import sys
import os
from matplotlib import pyplot as plt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Visuals import Visuals


class TestVisuals:
    def test_create_visuals_object(self):
        try:
            visuals = Visuals()
            assert True
        except:
            assert False
        