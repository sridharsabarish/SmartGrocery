import os

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
    months = ['June', 'July', 'August', 'September', 'October', 'November', 'December']
    for month in months:
        assert CheckPDFinDirectory(month)