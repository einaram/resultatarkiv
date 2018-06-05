import pyodbc 

class dbconnector:
    
    def listdata(table):
        sql = "search id,name from "+table
        


    def __init__(self):
        pass
    def fetchdict(self,sql,params=None):
        if params==None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql,params)
        columns = [column[0] for column in self.cursor.description]
        results=[]
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return(results)
        
    def connecttodb(self):
        self.server="Server=NRPA-3220\\SQLEXPRESS;"
        self.database="DataArkiv"
        #self.server="Server=databasix2\\databasix2;"
        connectstring="Driver={SQL Server Native Client 11.0};"+self.server+"Database="+self.database+";"+"Trusted_Connection=yes;Autocommit=False"
        cnxn = pyodbc.connect(
                      connectstring
                      )
        self.cursor = cnxn.cursor()
    
    def getcolumns(self):
        sql="select column_name,is_nullable,data_type,character_maximum_length from information_schema.columns where table_name=?"
        self.columns=self.fetchdict(sql,(self.tablename))
        
        
    def search(self):
        True
    
    