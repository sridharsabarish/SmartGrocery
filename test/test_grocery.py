import os
import pandas as pd
#from pypdf import PdfReader

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestPandas:
    def test_pandas_command(self):
        df = pd.DataFrame({"test_id": [1, 2, 3, 4, 5]})
    



    def test_createDFFromCSV(self):
        try:
            pd.read_csv('grocery_data.csv')
        except:
            AssertionError("Fail")
    
    
    def test_createDFFromCSVWrong(self):
        
        try:
            pd.read_csv('grocery_data2.csv')
        except:
            assert True
        

    def test_CheckPDFinDirectoryTestDirectoryIncorrect(self):
        
        try:
            if any(".pdf" in f for root, dirs, files in os.walk("test/") for f in files):
                assert False
            else:
                assert True
        except FileNotFoundError:
            print(f"Path {os.getcwd()} does not exist")
            assert True
    def test_CheckPDFinDirectoryTestDirectoryParentDirectory(self):
        
        try:
            if any(".pdf" in f for root, dirs, files in os.walk("..") for f in files):
                assert True
            else:
                assert False
        except FileNotFoundError:
            print(f"Path {os.getcwd()} does not exist")
            assert False
# def test_check_pdf_exists():
    # return false        

