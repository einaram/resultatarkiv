import pyodbc 
import collections
import os 
import configparser

def tree():
    return collections.defaultdict(tree)
    # Makes handling of multidimentional dicts easier

# Class for connection to the data base, contains also a few utility-functions to handle data

class dbconnector:
        
    def __init__(self):
        self.cursor=self.connecttodb()
        pass
    def checkuser(self,username,password):
        if self.cursor==None:
            self.connecttodb()
        authOK=False
        try:
            self.cursor.execute("select username,fullname,email,hashedpassword from users where username =? and hashedpassword=?",username,password)
            u=self.cursor.fetchall()
            authOK= len(u)==1
        # The only way to authenticate is if the sql ran well and returned one record
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
        if self.cursor==None:
            self.connecttodb()
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
        config=configparser.ConfigParser()
        config.read('database.ini')
        print(config)
        self.server=config['connection']['server']
        self.database=config['connection']['database']
        #self.server="Server=databasix2\\databasix2"
        #self.server="Server=NRPA-3220\\SQLEXPRESS;"
        #self.database="DataArkiv"
        #self.database="DataArkiv_tom"    
        connectstring="Driver={SQL Server Native Client 11.0};Server="+self.server+";Database="+self.database+";"+"Trusted_Connection=yes;Autocommit=False"
        self.cnxn = pyodbc.connect(connectstring)
        self.cursor = self.cnxn.cursor()
        print("connected ",self.server)
        scriptdir="sqlupdate"
        # Put sql-files with updates in the sqlupdate-subfolder
        # Preferably one sql-command per file, if more, they should be separated by ;
        # There cannot be any sql-comments in those files due to simple parsing
        for script in os.listdir(scriptdir):
            if not script.endswith(".sql"):
                continue
            sql="select count(id) from datafile where filename=?"
            self.cursor.execute(sql,script)
            if self.cursor.fetchall()[0][0]==0: # I.e. the file has not been run before
                with open(scriptdir+'\\' + script,'r') as inserts:
                    sqlScript = inserts.readlines()
                    sqlScript=" ".join(sqlScript)
                    for statement in sqlScript.split(';'):
                        try:
                            if statement=='':
                                continue
                            self.cursor.execute(statement)
                            self.cursor.commit()
                        except pyodbc.ProgrammingError as e:
                            print(e)
                        except pyodbc.IntegrityError as e:
                            print(e)
                sql="insert into datafile (filename,imported,md5) values(?,1,'none')"
            self.cursor.execute(sql,script)
            self.cursor.commit()
                   
        print("updates OK")
        
    
    def getcolumns(self,table=None):
        # Fetches information on all columns in active table
        if table==None:
            table=self.tablename
        sql="select column_name,is_nullable,data_type,character_maximum_length from information_schema.columns where table_name=?"
        self.columns=self.fetchdict(sql,(table))
    
    def getcolnames(self,table=None):
        # makes a list of the column names in the active table
        self.getcolumns(table)
        cols=[]
        for col in self.columns:
            cols.append(col['column_name'])
        self.colnames=cols
    
    def hash(self):
        if not hasattr(self,"columns") or self.columns==None:
            self.getcolumns()
        d={}
        for k in self.columns:
            col=k['column_name']
            try:
                d[col]=getattr(self,col)
            except AttributeError:
                d[col]=None
        return d
    
    
    