from xlrd import open_workbook
import xlrd
from xlrd.sheet import ctype_text 
import platform
import hashlib
import pyodbc 

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
        self.InvalidHeaderUnit = "Header '%s', column %i, has wrong unit. Is '%s' but this is not registered as a valid unit."
        self.InvalidHeaderUnitNuclide = "Nuclide header '%s', column %i, has wrong unit. Is '%s' but this is not registered as a valid unit."
        self.InvalidHeaderBase = "Header '%s', column %i, has wrong unit. Is '%s' but should be '%s'."
        self.InvalidHeader = "Header '%s' is not recognised as a valid header."
        self.InvalidNuclide = "Nuclide '%s', column %i,  is not recognised as valid. Is it registered in the database?"
        self.HeaderNonValidNuclide = "Header '%s' does not proceed a valid inital column of this nuclide, a column without any _* postfix. Last registered nuclide is '%s'."
        self.InvalidProjectid = "Project %s is not defined"
        self.OkHeader = "Header '%s' with unit %s is OK"
        self.InvalidArea = "Header '%s', column %i, has a wrong unit %s. Unit should be one of %s"
        self.ShortSummaryWrong = "Summary: %i headers were read, %i were ok and %i had errors. Please revise based on given messages."
        self.ShortSummaryRight = "Summary: %i headers were read and %i are ok. Congratulation."
        self.CheckDataMessage = "Checked data in column '%s' of type %s, and found %i row(s) with error. Rows with error are available from object '%s'"
        self.NotCheckDataMessage = "Did not check column '%s' of type %s, because it is a string."   
        self.ShortSummaryValidation = "Checked data in %i columns. %i are OK, and %i are not ok and should be checked based on error messages above."
        cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=NRPA-3220\\SQLEXPRESS;"
                      "Database=DataArkiv;"
                      "Trusted_Connection=yes;")
        self.cursor = cnxn.cursor()
        
        
    def check(self):
        self.md5=md5sum(self.file)
        wb = open_workbook(self.file)
        sht = wb.sheet_by_index(0)
        projecttype=sht.cell_value(0,0)
        if projecttype != 'PROJECTID':
            raise ValueError("Ukjent prosjekttype (A1)")
            # TODO: Define project in import file
        self.projectid=sht.cell_value(1,0)
        sql="select name from projects where id = ?"
        self.cursor.execute(sql,self.projectid)
        rows=self.cursor.fetchall()
        if len(rows)==0:
            raise ValueError("Project not defined")
        self.project=rows[0][0]
        if sht.cell_value(2,0) != "":
            raise ValueError("Forventet blank (A2)")
        self.fields=sht.row(3) 
        self.types=sht.row(4)
        
        

        
        
    def debug(self):
        print(self.project)
        print(self.md5)
        self.cursor.execute('Select * from projects')
        for row in self.cursor:
            print('row = %r' % (row,))
        
        
          
if __name__ == '__main__':
    test=excelfile('test.xlsx')
    test.check()
    test.debug()