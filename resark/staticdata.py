import pyodbc 

class metadatalist:
    
    def __init__(self,tablename,name=None,shortname=None,description=None,id=None,req=None):
        self.tablename=tablename
        if req !=None:
            for k,v in req.items():
                setattr(self,k,v)
            for k in ('name','shortname','description'):
                try:
                    if getattr(self,k)=='':
                        setattr(self,k,None)
                except AttributeError:
                    setattr(self,k,None)
        else:
            self.name=name
            self.shortname=shortname
            self.description=description
            self.id=id
        try:
            if self.shortname != None:
                self.shortname=self.shortname.upper()
        except AttributeError:
            # if so, just ignore it.
            True
        self.columns=None
        self.cursor=None
    
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
        sql="select column_name,is_nullable,data_type,character_maximum_length from information_schema.columns where table_name=?"
        self.columns=self.fetchdict(sql,(self.tablename))
        
        
        
    def fields(self):
        d={}
        for k in self.columns:
            col=k['column_name']
            try:
                d[col]=getattr(self,col)
            except AttributeError:
                d[col]=None
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
        
        sql = "select id,"+",".join(self.dynfields()) +" from "+self.tablename
        if len(values)>0:
            sql=sql+" where "+(" and ".join(fields))
        self.cursor.execute(sql,values)
        set = self.cursor.fetchall()
        return(set)
    
    def dynfields(self):
        fields=list(self.fields().keys())
        fields.remove('id')
        return(fields)
        
    def save(self):
        if self.cursor==None:   
            self.connecttodb()
        
        fields=self.dynfields()
        sql="insert into "+self.tablename +"("+",".join(fields)+") values("+",".join('?'*len(fields)) +")"
        param=[]
        for field in fields:
            param.append(getattr(self,field))
        self.cursor.execute(sql,param)
        self.cursor.commit()
        print("Saving")