from xlrd import open_workbook
import platform
import hashlib


# Valid excel?
# correct setup for import
# Run validation
# Check if values makes sense
# Check for new values
# Abort if errors needs to be corrected
# Ask for verification if new values are OK
# Import if verified

def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()



class excelfile:
    def __init__(self,file):
        self.file=file
        
    def check(self):
        self.md5=md5sum(self.file)
        wb = open_workbook(self.file)
        sht = wb.sheet_by_index(0)
        projecttype=sht.cell_value(0,0)
        if projecttype != 'PROJECTID':
            raise ValueError("Ukjent prosjekttype (A1)")
        self.project=sht.cell_value(1,0)
        if sht.cell_value(2,0) != "":
            raise ValueError("Forventet blank (A2)")
        
    def debug(self):
        print(self.project)
        print(self.md5)
    
    
if __name__ == '__main__':
    test=excelfile('test.xlsx')
    test.check()
    test.debug()