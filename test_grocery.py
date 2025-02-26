import os
import pandas as pd
#from pypdf import PdfReader


def test_pandas_command():
    df = pd.DataFrame({"test_id": [1, 2, 3, 4, 5]})
   



def test_createDFFromCSV():
    try:
        pd.read_csv('grocery_data.csv')
    except:
        AssertionError("Fail")
    
    
def test_createDFFromCSVWrong():
    
    try:
        pd.read_csv('grocery_data2.csv')
    except:
        assert True
    
    
def CheckPDFinDirectory(path):
    
    try:
        if any(".pdf" in f for f in os.listdir(path)):
            return True
        else:
            return False
    except FileNotFoundError:
        print(f"Path {path} does not exist")
        return False

def test_check_pdf_exists():
    # Months to be modified according to files.
    months = ['June', 'July', 'August', 'September', 'October', 'November', 'December']
    for month in months:
        assert CheckPDFinDirectory(month)
        

