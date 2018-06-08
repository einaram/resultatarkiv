import pyodbc 
import collections

def tree():
    return collections.defaultdict(tree)
    # Makes handling of multidimentional dicts easier



class dbconnector:
    
    def listdata(table):
        sql = "search id,name from "+table
        


    def __init__(self):
        self.cursor=None
        pass
    def checkuser(self,username,password):
        if self.cursor==None:
            self.connecttodb()
        authOK=False
        try:
            self.cursor.execute("select username,fullname,email,hashedpassword from users where username =? and hashedpassword=?",username,password)
            u=self.cursor.fetchall()
            authOK= len(u)==1
        except pyodbc.DataError:
            authOK=False
        except IndexError:
            authOK=False
        return(authOK)

        
    def fetchlist(self,sql):
        self.cursor.execute(sql)
        list=[]
        row = self.cursor.fetchone()
        while row is not None:
            list.append(row[0])
            row = self.cursor.fetchone()     
        return(list)
    
    def listnames(self,table):
        sql = "select id,name from "+table+" order by name"
        self.cursor.execute(sql)
        table=self.cursor.fetchall()
        return(table)
    
    
    
        
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
        self.cnxn = pyodbc.connect(
                      connectstring
                      )
        self.cursor = self.cnxn.cursor()
        print("connecting ",self.server)
    
    
    def getcolumns(self,table=None):
        if table==None:
            table=self.tablename
        sql="select column_name,is_nullable,data_type,character_maximum_length from information_schema.columns where table_name=?"
        self.columns=self.fetchdict(sql,(table))
    
    def getcolnames(self,table=None):
        self.getcolumns(table)
        cols=[]
        for col in self.columns:
            cols.append(col['column_name'])
        self.colnames=cols
    
    def hash(self):
        if self.columns==None:
            self.getcolumns()
        d={}
        for k in self.columns:
            col=k['column_name']
            try:
                d[col]=getattr(self,col)
            except AttributeError:
                d[col]=None
        return d
    
    def search(self):
        True
    
    