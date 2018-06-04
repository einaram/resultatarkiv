import pyodbc 

class metadatalist:
    
    def __init__(self,name=None,shortname=None,description=None,id=None,req=None):
        print("start")
        if req !=None:
            self.name=req['name']
            self.shortname=req['shortname']
            self.description=req['description']
            if self.name=='':
                self.name=None
            if self.shortname=='':
                self.shortname=None
            
            if self.description=='':
                self.description=None
        else:
            self.name=name
            self.shortname=shortname
            self.description=description
            self.id=id
        if self.shortname != None:
            self.shortname=self.shortname.upper()
        self.cursor=None
        
    def connecttodb(self):
        self.server="Server=NRPA-3220\\SQLEXPRESS;"
        self.database="DataArkiv"
        #self.server="Server=databasix2\\databasix2;"
        connectstring="Driver={SQL Server Native Client 11.0};"+self.server+"Database="+self.database+";"+"Trusted_Connection=yes;Autocommit=False"
        cnxn = pyodbc.connect(
                      connectstring
                      )
        self.cursor = cnxn.cursor()
        
    def fields(self):
        d={"name": self.name,"shortname": self.shortname,"description":self.description}
        return d
    
    def search(self,n=None,partial=True):
        # TODO: Return a limited number of values
        if self.cursor==None:
            self.connecttodb()
        fields=[]
        values=[]
        for k,v in self.fields().items():
            if v != None:
                if partial:
                    fields.append(k+" like ?")
                    values.append("%%"+v+"%%")
                else:
                    fields.append(k+"=?")
                    values.append(v)
        sql = "select id,name,shortname,description from metadatalist"
        if len(values)>0:
            sql=sql+" where "+(" and ".join(fields))
        self.cursor.execute(sql,values)
        set = self.cursor.fetchall()
        return(set)
        
        
    def save(self):
        if self.cursor==None:   
            self.connecttodb()
        sql="insert into metadatalist (name,shortname,description) values(?,?,?)"
        self.cursor.execute(sql,self.name,self.shortname,self.description)
        self.cursor.commit()
        print("Saving")