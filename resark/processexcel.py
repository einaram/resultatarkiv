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
        self.ExpectedBlank = "Forventet blank (%s)"
        
        self.server="Server=NRPA-3220\\SQLEXPRESS;"
        #self.server="Server=databasix2\\databasix2;"
        connectstring="Driver={SQL Server Native Client 11.0};"+self.server+"Database=DataArkiv;"+"Trusted_Connection=yes;"
        cnxn = pyodbc.connect(
                      connectstring
                      )
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
            raise ValueError(self.InvalidProjectid)
        self.project=rows[0][0]
        if sht.cell_value(2,0) != "":
            raise ValueError(self.ExpectedBlank)
        self.fields=sht.row(3) 
        self.types=sht.row(4)
        sql="select top 10 shortname,attrtype,datatype,name from validData where not shortname is null"
        self.cursor.execute(sql)
        validData=self.cursor.fetchall()
        # Count validated rows
        OK=0
        WRONG=0
        sqlValid="select count(shortname) from validData where shortname=? and attrtype!='NUCLIDE'"
        self.ShortnameStatus=[]
        colnr=0
        for field,type in zip(self.fields,self.types):
            param=type.value
            if param == "METADATA" or param == "BASE":
                param=field.value
            self.cursor.execute(sqlValid,param)
            valid=self.cursor.fetchall()
            self.ShortnameStatus.append(valid[0][0])
            print(field.value,type.value,valid[0][0])
        print(self.ShortnameStatus)
        

        
        
    def debug(self):
        print(self.project)
        print(self.md5)
        
        
          
if __name__ == '__main__':
    test=excelfile('test.xlsx')
    test.check()
    test.debug()