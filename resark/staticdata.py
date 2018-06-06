import pyodbc 

from .dbconnector import *

class metadatalist(dbconnector):

#TODO: Presenter og editer data med foreign key-kobling

    
    def __init__(self,tablename,name=None,shortname=None,description=None,id=None,req=None):
        self.tablename=tablename
        if req !=None:
            for k,v in req.items():
                if v=='':
                    setattr(self,k,None)
                else:
                    setattr(self,k,v)
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
    
    
        
    
    def search(self,n=None,partial=True):
        # TODO: Return a limited number of values
        if self.cursor==None:
            self.connecttodb()
        fields=[]
        values=[]
        for k,v in self.hash().items():
            print(k,v)
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
        print(sql)
        print(values)
        self.cursor.execute(sql,values)
        set = self.cursor.fetchall()
        return(set)
    
    def dynfields(self):
        fields=list(self.hash().keys())
        fields.remove('id')
        return(fields)
        
    def fields(self):
        if self.cursor==None:   
            self.connecttodb()
        return(list(self.hash().keys()))
        
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