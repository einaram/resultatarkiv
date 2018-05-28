from xlrd import open_workbook
import xlrd
from xlrd.sheet import ctype_text 
import platform
import hashlib
import pyodbc 
import re
import collections
import time
import sys
import datetime


# Valid excel?
# correct setup for import
# Run validation
# Check if values makes sense
# Check for new values where that should be checked
# Abort if errors needs to be corrected
# Ask for verification if new values are OK
# Import if verified

def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


 
# Function to return Excel column name 
# for a given column number
def colname(n):
    n=n+1 # using 0-based col numbering
    # To store result (Excel column name)
    string = []
    # To store current index in str which is result
    while n > 0:
        # Find remainder
        rem = n % 26
        # if remainder is 0, then a 
        # 'Z' must be there in output
        if rem == 0:
            string.append('Z')
            n = int(n / 26) - 1
        else:
            string.append(chr((int(rem) - 1) + ord('A')))
            n = int(n / 26)
 
    # Reverse the string and return result
    string = string[::-1]
    return "".join(string)

def cellname(col,row):
    c=colname(col)
    r=str(row)
    return(c+r)
    
def tree():
    return collections.defaultdict(tree)
    # Makes handling of multidimentional dicts easier
    

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
        self.invalidValue = "%s has an invalid value"
        self.OkHeader = "Header '%s' with unit %s is OK"
        self.InvalidArea = "Header '%s', column %i, has a wrong unit %s. Unit should be one of %s"
        self.ShortSummaryWrong = "Summary: %i headers were read, %i were ok and %i had errors. Please revise based on given messages."
        self.ShortSummaryRight = "Summary: %i headers were read and %i are ok. Congratulation."
        self.CheckDataMessage = "Checked data in column '%s' of type %s, and found %i row(s) with error. Rows with error are available from object '%s'"
        self.NotCheckDataMessage = "Did not check column '%s' of type %s, because it is a string."   
        self.ShortSummaryValidation = "Checked data in %i columns. %i are OK, and %i are not ok and should be checked based on error messages above."
        self.ExpectedBlank = "Forventet blank (%s)"
        self.invalidColOrder = "%s må komme før %s"
        self.invalidDate="Feil dato - må være åååå.mm.dd evt med tt:mm:ss"
        self.warningEmpty="%s has no data"
        self.errorUnhandeled="Ikke-håndterte data, sjekk at headere er riktige"
        
        self.sqlValidNoNuc="select count(shortname) from validData where shortname=? and attrtype!='NUCLIDE'"
        self.sqlValidGetParam="select count(shortname) from validData where shortname=? and attrtype=?"
        self.sqlValidSubtype="select count(stl.id) from samplesubtypelist sstl left join sampletypelist stl on stl.id=sampletypelistid where stl.shortname=? and sstl.name =?"    
        self.sqlValidMetadata="select count(smd.id) from samplemetadata smd left join metadatalist md on smd.metadataid=md.id where md.shortname=? and smd.value=?"
        self.sqlValidLaboratory="select count(id) from samplevalue where laboratory = ?"
        self.sqlValidUncmethod="select count(id) from samplevalue where uncmeasure = ?"
        self.sqlValidInstrument="select count(id) from samplevalue where instrument = ?"
        self.sqlValidSpecies="select count(sp.id) from specieslist sp left join sampletypelist st on sp.sampletypeid = st.id where sp.id=? and st.shortname=?"
        self.sqlValidAreaId="select count(areaid) from GeoAreas where objtype=? and areaid=?"
        
        self.nuclide=[]
        self.ShortnameStatus=[]
        self.server="Server=NRPA-3220\\SQLEXPRESS;"
        self.database="DataArkiv"
        #self.server="Server=databasix2\\databasix2;"
        connectstring="Driver={SQL Server Native Client 11.0};"+self.server+"Database="+self.database+";"+"Trusted_Connection=yes;"
        cnxn = pyodbc.connect(
                      connectstring
                      )
        self.cursor = cnxn.cursor()
        self.valuewarning=tree()
        self.valueerror=tree()
        self.SEENBEFORE=1
        self.headerRows=5
        self.lookup=tree()
        self.dateFormat=None
        
    def check(self):
        self.ShortnameStatus=[]
        self.checkheader()
        if self.validheader:
            self.checkdata()
    
    def checkItemEmptyOK(self,type,shortname,cell,sql,col,row,message):
        valid=self.lookup[type][shortname][cell.value]==1
        if not valid:
            self.cursor.execute(self.sqlValidUncmethod,cell.value)
            valid=(self.cursor.fetchall()[0][0]>0 or cell.ctype==xlrd.XL_CELL_EMPTY)    
            if not valid:
                self.addvaluewarning(message,col,row,cell.value)
                warning=True
            else:
                self.lookup[type][shortname][cell.value]=1

    
    def checkdata(self):
        if len(self.ShortnameStatus)==0:
            raise ValueError(self.InvalidProjectid)
        # Jumps out if either the header has not been processed or it has errors
        col=0
        validvalues=[]
        valueerror={}
        sampletypecol=-1
        parentcol=-1
        parentdata=[]
        nonhandeled=0
        laboratory=[] # Workaround until database is updated with index on laboratory search ZZZ
        units=[]
        allowNewValues=["SAMPLEID","LIMSNR"] # Will accept new values for metadata
        
        sql="select shortname from unitlist"
        for row in self.cursor.execute(sql):
            units.append(row[0])
        lookup=tree() # Buffer to store valid data - to avoid data base lookups
        for shortname,type in zip(self.fields,self.types):
		# shortname: row 4
        # type: row 5
            starttime=time.time()
            xlcol=list(self.sht.col(col))
            del xlcol[:self.headerRows] # remove five first to get rid of headers
            row=5
            doneOnce=False
            for cell in xlcol:
                valid=False
                warning=False
                if type.value=="VALUE":
                    valid= cell.ctype in [xlrd.XL_CELL_EMPTY,xlrd.XL_CELL_NUMBER]
                elif shortname.value=="PARENT_ID":
                    # Anything is valid here, may need it later on for connection
                    parentcol=col
                    if len(parentdata)==0:
                        for p in xlcol:
                            if p.ctype !=xlrd.XL_CELL_EMPTY:
                                parentdata.append(p.value)
                    valid=True
                elif shortname.value=="CONNECT_TO_PARENT":
                    # Should have a valid parent_id
                    if cell.ctype==xlrd.XL_CELL_EMPTY:
                        valid=True
                    else:
                        if len(parentdata)==0:
                            raise ValueError(self.invalidColOrder)
                        valid=(parentdata.count(cell.value)>0 or cell.ctype==xlrd.XL_CELL_EMPTY)
                elif type.value == "AREAID":
                    seen=False
                    value=cell.value
                    if cell.ctype==xlrd.XL_CELL_NUMBER:
                        value=str(int(value))
                    if shortname.value=="KOMMUNE":
                        if len(value)==3:
                            value="0"+value
                    if value in lookup[shortname.value][type.value]:
                        valid=(lookup[shortname.value][type.value][value]==1) or (cell.ctype==xlrd.XL_CELL_EMPTY)
                        seen=True
                    valid = valid or cell.ctype == xlrd.XL_CELL_EMPTY
                    if not (seen or valid):
                        self.cursor.execute(self.sqlValidAreaId,shortname.value,value)
                        print("SQL:"+value)
                        res=self.cursor.fetchall()[0][0]
                        print(res)
                        valid=(res>0 or cell.ctype==xlrd.XL_CELL_EMPTY)
                        if not valid:
                            key="Unknown metadatavalue for %s" % shortname.value
                            warning=True
                            lookup[shortname.value][type.value][value]=-1
                        else:
                            lookup[shortname.value][type.value][value]=1
                    if not valid:
                        key="Unknown metadatavalue for %s" % shortname.value
                        self.addvaluewarning(key,col,row,value)
                        warning=True
                    
                elif shortname.value=="SAMPLETYPE":
                    # Valid if sampletype is defined
                    sampletypecol=col # Possible need to look up from subtype or species
                    value=cell.value
                    valid=(lookup[shortname.value][type.value][value]==1)
                    if not valid:
                        self.cursor.execute(self.sqlValidGetParam,cell.value, shortname.value)
                        valid=(self.cursor.fetchall()[0][0]>0 and cell.ctype != xlrd.XL_CELL_EMPTY)
                        if valid:
                            lookup[shortname.value][type.value][value]=1
                elif shortname.value=="SAMPLESUBTYPE":
                    # Valid if subtype is defined and correct for sampletype
                    if sampletypecol < 0:
                        raise ValueError(invalidColOrder % ('Sampletype','Subtype'))
                    sampletype=self.sht.cell_value(row,sampletypecol)
                    self.cursor.execute(self.sqlValidSubtype,sampletype,cell.value)
                    valid=cell.ctype==xlrd.XL_CELL_EMPTY or self.cursor.fetchall()[0][0]>0
                elif shortname.value=="REF_DATE" or shortname.value=="SAMPLE_DATE":
                    # Any date is valid
                    valid=cell.ctype==xlrd.XL_CELL_DATE
                    if not valid:
                        dateparts=list(filter(None, re.split(r'(\d+)',cell.value)))
                        try:
                            if(self.dateFormat==None):
                                if len(dateparts)<5 or len(dateparts) > 11:
                                    raise ValueError(self.invalidDate)
                                dsep=dateparts[1]
                                if len(dateparts[0])==4:
                                    self.dateFormat="%Y"+dsep+"%m"+dsep+"%d"
                                if len(dateparts[4])==4:
                                    self.dateFormat="%d"+dsep+"%m"+dsep+"%Y"
                                if self.dateFormat==None:
                                    raise ValueError(self.invalidDate)
                                if len(dateparts) >5:
                                    hsep=dateparts[7]
                                    self.dateFormat=self.dateFormat+dateparts[5]+"%H"+hsep+"%M"
                                if len(dateparts) >9:
                                    self.dateFormat=self.dateFormat+hsep+"%S"
                            datetime.datetime.strptime(cell.value,self.dateFormat)
                            valid=True # Will be trown out if parsing does not work
                        except ValueError:
                            valid=False
                            self.addvalueerror(self.invalidDate,col,row,cell.value)
                elif shortname.value == "LATITUDE":
                    # Valid numbers from -90 to 90- inclusive
                    if cell.ctype==xlrd.XL_CELL_EMPTY:
                        self.addvaluewarning(self.warningEmpty% "LATITUDE",col,row,"No data")
                    else:
                        valid=(cell.ctype==xlrd.XL_CELL_NUMBER and  cell.value >=-90 and cell.value <=90)
                        if not valid:
                            self.addvalueerror(self.invalidValue % shortname.value,col,row,cell.value)
                elif shortname.value == "LONGITUDE":
                    if cell.ctype==xlrd.XL_CELL_EMPTY:
                        self.addvaluewarning(self.warningEmpty% shortname.value,col,row,"No data")
                    else:
                    # Valid numbers from -180 to 180 - inclusive
                        valid=(cell.ctype==xlrd.XL_CELL_EMPTY) or (cell.ctype==xlrd.XL_CELL_NUMBER and  cell.value >=-180 and cell.value <=180)
                        if not valid:
                            self.addvalueerror("Invalid value for %s" % cell.value,col,row,cell.value)
                elif type.value == "UNCMETHOD" or shortname.value.endswith("_UNCMEASURE"):
                    self.checkItemEmptyOK(type.value,shortname.value,cell,self.sqlValidUncmethod,col,row,"Unknown uncertainty definition")
                elif type.value == "UNCMETHOD0" or shortname.value.endswith("_UNCMEASURE0"):
                    valid=lookup["UNCMETHOD"][shortname.value][cell.value]==1
                    if not valid:
                        self.cursor.execute(self.sqlValidUncmethod,cell.value)
                        valid=(self.cursor.fetchall()[0][0]>0 or cell.ctype==xlrd.XL_CELL_EMPTY)    
                        if not valid:
                            key="Unknown uncertainty definition"
                            self.addvaluewarning(key,col,row,cell.value)
                            warning=True
                        else:
                            lookup["UNCMETHOD"][shortname.value][cell.value]=1
                elif type.value == "INSTRUMENT" or shortname.value.endswith("_INSTRUMENT"):
                    valid=lookup["INSTRUMENT"][shortname.value][cell.value]==1
                    if not valid:
                        self.cursor.execute(self.sqlValidInstrument,cell.value)
                        valid=(self.cursor.fetchall()[0][0]>0 or cell.ctype==xlrd.XL_CELL_EMPTY)    
                        if not valid:
                            key="Unknown uncertainty definition"
                            self.addvaluewarning(key,col,row,cell.value)
                            warning=True
                        else:
                            lookup["INSTRUMENT"][shortname.value][cell.value]=1
                elif shortname.value == "WEEKNR":
                    valid = cell.ctype==xlrd.XL_CELL_EMPTY or (cell.ctype==xlrd.XL_CELL_NUMBER  and cell.value > 0 and cell.value < 54)
                elif type.value == "METADATA" and shortname.value in allowNewValues:
                    valid=True
                elif type.value == "METADATA":
                    # Valid if value for metadata has been seen before
                    # Need a warning for new value, invalid for new key
                    # print(colname(col),row)
                    seen=False
                    value=cell.value
                    if value in lookup["METADATA"][shortname.value]:
                        valid=lookup["METADATA"][shortname.value][value]==1
                        seen=True
                    if not seen:
                        self.cursor.execute(self.sqlValidMetadata,shortname.value,str(value))
                        valid=(cell.ctype==xlrd.XL_CELL_EMPTY or self.cursor.fetchall()[0][0]>0)
                        if not valid:
                            if cell.ctype==xlrd.XL_CELL_NUMBER:
                                value=int(value)
                                self.cursor.execute(self.sqlValidMetadata,shortname.value,str(value))
                                valid=(self.cursor.fetchall()[0][0]>0 or cell.ctype==xlrd.XL_CELL_EMPTY)
                            else:
                                lookup["METADATA"][shortname.value][value]=1
                        else:
                            lookup["METADATA"][shortname.value][value]=1
                    if not valid:
                        key="Unknown metadatavalue for %s" % shortname.value
                        self.addvaluewarning(key,col,row,cell.value)
                        warning=True
                        lookup["METADATA"][shortname.value][value]=-1
            
                elif shortname.value == "SPECIESID":
                    
                    sampletype=self.sht.cell_value(row,sampletypecol)
                    self.cursor.execute(self.sqlValidSpecies,cell.value,sampletype)
                    valid=(self.cursor.fetchall()[0][0]>0 or cell.ctype==xlrd.XL_CELL_EMPTY)
                    
                elif type.value == "LABORATORY":
                    # Valid if laboratory seen before or empty
                    # Todo: Either add index on laboratory (need to change the col to varchar(100))  
                    valid=(laboratory.count(cell.value)>0) # workaround ZZZ
                    if not valid: # workaround ZZZ
                        self.cursor.execute(self.sqlValidLaboratory,cell.value)
                        valid=(self.cursor.fetchall()[0][0]>0 or cell.ctype==xlrd.XL_CELL_EMPTY)
                        if valid: # workaround ZZZ
                            laboratory.append(cell.value)
                elif units.count(type.value): # This is a number
                    valid=(cell.ctype==xlrd.XL_CELL_NUMBER or cell.ctype==xlrd.XL_CELL_EMPTY)
                elif shortname.value=="COMMENT":
                    valid=True
                elif shortname.value=="COMMENTS":
                    valid=True
                else: 
                    if not cell.ctype==xlrd.XL_CELL_EMPTY:
                       # print(type.value,shortname.value,cell.value)
                       self.addvalueerror(self.errorUnhandeled,col,row,cell.value)
                    nonhandeled=nonhandeled+1 
                if (not valid) and (not warning):
                   False
                   # print(colname(col)+str(row+1))
                row=row+1
            # print(col,sampletypecol) 
            elaps=time.time()-starttime
            print("Kolonne:",colname(col)," ",shortname.value," ",type.value," tid:",elaps)
            col = col +1
        self.nonhandeled=nonhandeled
        
    def addvalueerror(self,key,col,row,value):
        cellid=colname(col)+str(row+2) # Need +2 for some reason...
        if self.valueerror[key][value]=={}:
            self.valueerror[key][value]=[cellid]
        else:
            self.valueerror[key][value].append(cellid)
        
       
    def addvaluewarning(self,key,col,row,value):
        # using zero-based row numbers
        cellid=colname(col)+str(row+2) # Need +2 for some reason...
        if self.valuewarning[key][value]=={}:
            self.valuewarning[key][value]=[cellid]
        else:
            self.valuewarning[key][value].append(cellid)
         
         
         
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
        if self.sht.cell_value(3,0) == "":
            self.headerRows=6
        self.fields=self.sht.row(self.headerRows-2) 
        self.types=self.sht.row(self.headerRows-1)
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
        
    def validdata(self):
        valid = len(self.validvalues) > 0
        valid = valid and self.validvalues.count(False) == 0
        return valid
        
    def debug(self):
        print(self.project)
        print(self.md5)
        # print(self.ShortnameStatus)
        # print("True:",self.validvalues.count(True))
        # print("False:",self.validvalues.count(False))
        print("Nonhandeled:",self.nonhandeled)
        #print(self.valuewarning)
        # print(self.valueerror)
          
if __name__ == '__main__':
    if(len(sys.argv)==1):
        file="RAME kyststasjoner.xlsx"
    else:
        file=sys.argv[1]
    dir="C:\\Users\\mortens\\SharePoint\\Resultatarkivet - Dokumenter\\Forsøk på koding av datasett\\"
    # dir="..\\testdata\\"
    test=excelfile(dir+file)
    test.check()
    test.debug()