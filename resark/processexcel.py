from xlrd import open_workbook
import xlrd
from xlrd.sheet import ctype_text 
import platform
import hashlib
import pyodbc 
import re


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
        self.invalidColOrder = "%s må komme før %s"
        self.sqlValidNoNuc="select count(shortname) from validData where shortname=? and attrtype!='NUCLIDE'"
        self.sqlValidGetParam="select count(shortname) from validData where shortname=? and attrtype=?"
        self.sqlValidSubtype="select count(stl.id) from samplesubtypelist sstl left join sampletypelist stl on stl.id=sampletypelistid where stl.shortname=? and sstl.name =?"    
        self.sqlValidMetadata="select count(smd.id) from samplemetadata smd left join metadatalist md on smd.metadataid=md.id where md.shortname=? and smd.value=?"
        self.nuclide=[]
        self.ShortnameStatus=[]
        self.server="Server=NRPA-3220\\SQLEXPRESS;"
        #self.server="Server=databasix2\\databasix2;"
        connectstring="Driver={SQL Server Native Client 11.0};"+self.server+"Database=DataArkiv;"+"Trusted_Connection=yes;"
        cnxn = pyodbc.connect(
                      connectstring
                      )
        self.cursor = cnxn.cursor()
        
    def check(self):
        self.ShortnameStatus=[]
        self.checkheader()
        if self.validheader:
            self.checkdata()
    
    
    def checkdata(self):
        if len(self.ShortnameStatus)==0:
            raise ValueError(self.InvalidProjectid)
        # Jumps out if either the header has not been processed or it has errors
        col=0
        validvalues=[]
        sampletypecol=-1
        parentcol=-1
        parentdata=[]
        nonhandeled=0
        for shortname,type in zip(self.fields,self.types):
		# shortname: dataHeader[1,]
        # type:  dataHeader[2,]
            xlcol=list(self.sht.col(col))
            # print(xlcol)
            del xlcol[:5] # remove five first to get rid of headers
            # print(xlcol)
            # print(shortname)
            row=5
            for cell in xlcol:
                valid=False
                if shortname.value=="PARENT_ID":
                    parentcol=col
                    if len(parentdata)==0:
                        for p in xlcol:
                        #    print(p)
                            if p.ctype !=xlrd.XL_CELL_EMPTY:
                                parentdata.append(p.value)
                        # print(parentdata)
                    valid=True
                elif shortname.value=="CONNECT_TO_PARENT":
                    if len(parentdata)==0:
                        raise ValueError(invalidColOrder)
                    # print(cell.value)
                    # print(parentdata.count(cell.value))
                    valid=(parentdata.count(cell.value)>0 or cell.ctype==xlrd.XL_CELL_EMPTY)
                    # print(valid)
                elif shortname.value=="SAMPLETYPE":
                    sampletypecol=col
                    self.cursor.execute(self.sqlValidGetParam,cell.value, "SAMPLETYPE")
                    valid=self.cursor.fetchall()[0][0]
                elif shortname.value=="SAMPLESUBTYPE":
                    if sampletypecol < 0:
                        raise ValueError(invalidColOrder % ('Sampletype','Subtype'))
                    sampletype=self.sht.cell_value(row,sampletypecol)
                    self.cursor.execute(self.sqlValidSubtype,sampletype,cell.value)
                    valid=self.cursor.fetchall()[0][0]
                elif shortname.value=="REF_DATE":
                    valid=cell.ctype==xlrd.XL_CELL_DATE
                    # print(cell.value,cell.ctype,valid)
                elif shortname.value == "LATITUDE":
                    valid=(cell.ctype==xlrd.XL_CELL_NUMBER and  cell.value >=-90 and cell.value <=90)
                elif shortname.value == "LONGITUDE":
                    valid=(cell.ctype==xlrd.XL_CELL_NUMBER and  cell.value >=-180 and cell.value <=180)
                elif type.value == "METADATA":
                    self.cursor.execute(self.sqlValidMetadata,shortname.value,cell.value)
                    valid=(self.cursor.fetchall()[0][0]>0 or cell.ctype==xlrd.XL_CELL_EMPTY)
                   # print(cell.value,valid)
                else: 
                    nonhandeled=nonhandeled+1
                validvalues.append(valid)
                row=row+1
            # print(col,sampletypecol)
            col = col +1
        self.validvalues=validvalues
        self.nonhandeled=nonhandeled
        
        
    def checkheader(self):
        self.md5=md5sum(self.file)
        wb = open_workbook(self.file)
        self.sht = wb.sheet_by_index(0)
        projecttype=self.sht.cell_value(0,0)
        if projecttype != 'PROJECTID':
            raise ValueError("Ukjent prosjekttype (A1)")
            # TODO: Define project in import file
        self.projectid=self.sht.cell_value(1,0)
        sql="select name from projects where id = ?"
        self.cursor.execute(sql,self.projectid)
        rows=self.cursor.fetchall()
        if len(rows)==0:
            raise ValueError(self.InvalidProjectid)
        self.project=rows[0][0]
        if self.sht.cell_value(2,0) != "":
            raise ValueError(self.ExpectedBlank)
        self.fields=self.sht.row(3) 
        self.types=self.sht.row(4)
        # sql="select shortname,attrtype,datatype,name from validData where not shortname is null"
        # self.cursor.execute(sql)
        # validData=self.cursor.fetchall()
        # Count validated rows
        self.ShortnameStatus=[]
        ## Regular expression for checking for valid nuclide format
        regexpnuc='^[A-Z]{1,2}([0-9]{1,3}m{0,1}){0,1}(\\_{0,1}[0-9]{0,3}){0,1}(\\#{0,1}[0-9]{0,9}){0,1}$'
        for field,type in zip(self.fields,self.types):
        # field: dataHeader[1,]
        # type:  dataHeader[2,]
            valid=0
            param=type.value
            if param == "METADATA" or param == "BASE":
                param=field.value
            self.cursor.execute(self.sqlValidNoNuc,param)
            valid=self.cursor.fetchall()[0][0]
            if type.value == 'AREAID':
                self.cursor.execute(self.sqlValidGetParam,param, "AREA")
                valid=self.cursor.fetchall()[0][0]
            if valid == 0:
                self.cursor.execute(self.sqlValidGetParam,param, "QUANTITY")
                n=self.cursor.fetchall()[0][0]
                if n==1:
                    self.cursor.execute(self.sqlValidGetParam,type.value, "UNIT")
                    valid=self.cursor.fetchall()[0][0]
                
            # Valid should be either 1 or 0 - depending if the shortname exists or not.
            nuclide=False
            if valid == 0: # Probably nuclide
                nuclide=True
                c_nucl=""
                nucl=field.value.split("_")
                if len(nucl)==3:
                    c_nucl = nucl[0]+"_"+nucl[1]
                    c_ctrl = nucl[2]
                elif len(nucl)==1:
                    c_nucl=nucl[0]
                    c_ctrl=None 
                else:
                    self.cursor.execute(self.sqlValidGetParam,nucl[1], "VALUE")
                    validnuc=self.cursor.fetchall()[0][0]
                    if validnuc ==1:
                        c_nucl=nucl[0]
                        c_ctrl=nucl[1]
                    else:
                        c_nucl = nucl[0]+"_"+nucl[1]
                        c_ctrl = None
                # print("nucl:",nucl)
                # print("c_nucl:",c_nucl)
                m=re.search(regexpnuc,c_nucl)
                if m != None:
                    basenuc=c_nucl.split("#")
                    self.cursor.execute(self.sqlValidGetParam,basenuc[0], "NUCLIDE")
                    validnuc=self.cursor.fetchall()[0][0]
                    if validnuc == 1:
                        if c_ctrl == None:
                            current_nuclide=c_nucl
                            self.cursor.execute(self.sqlValidGetParam,type.value, "UNITS")
                            valid=self.cursor.fetchall()[0][0]
                        else:
                           # if current_nuclide == c_nucl: # This is a bug, this will never be true
                            self.cursor.execute(self.sqlValidGetParam,c_ctrl, "VALUE") 
                            valid=self.cursor.fetchall()[0][0]
                 #   print(basenuc)
                else:
                    valid=0
                    nuclide=False
            self.ShortnameStatus.append(valid)
            self.nuclide.append(nuclide)
            #print(field.value,type.value,valid)
        #print(self.ShortnameStatus)
        # print(self.nuclide)

    def validheader(self):
        valid = len(self.ShortnameStatus) > 0
        valid = valid and not 0 in self.ShortnameStatus
        return valid
        
    def debug(self):
        print(self.project)
        print(self.md5)
        # print(self.ShortnameStatus)
        print("True:",self.validvalues.count(True))
        print("False:",self.validvalues.count(False))
        print("Nonhandeled:",self.nonhandeled)
          
if __name__ == '__main__':
    test=excelfile('test.xlsx')
    test.check()
    test.debug()