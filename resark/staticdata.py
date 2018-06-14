import pyodbc 

from .dbconnector import *

class metadatalist(dbconnector):

#TODO: Presenter og editer data med foreign key-kobling

    
    def __init__(self,tablename,name=None,shortname=None,username=None,description=None,id=None,req=None):
        # Initieres helst med req - som kan hentes fra request.form
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
            self.username=username
            self.id=id
        try:
            if self.shortname != None:
                self.shortname=self.shortname.upper()
        except AttributeError:
            # if so, just ignore it - there is no shortname - maybe better to explicitely ask if the attribute exists
            True
        self.columns=None
        self.cursor=self.connecttodb()
    
    
    def checkexists(self,req,uniquefields=["name","shortname"]):
        #for f in uniquefields:
        #    if getattr(self,f)!=None - bygge opp sql...
        sql = "select count (id) from "+self.tablename +" where name=? or shortname =?"
        print(sql)
        self.cursor.execute(sql,self.name,self.shortname)
        return(self.cursor.fetchall()[0][0])
        
    
    def search(self,partial=True):
        # partial - searches for a string anywhere within a field
        # TODO: Return a limited number of values
        fields=[]
        values=[]
        for k,v in self.hash().items():
            print(k,v)
            if v != None:
                v=str(v)
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
        # Lists the user-definable fiels a table
        fields=list(self.hash().keys())
        try:
            fields.remove('id')
        except:
            pass # Id did not exist - I do not care
        return(fields)
        
    def fields(self):
        # Returns a list of all fields in the actual table
        return(list(self.hash().keys()))
        
        
    def save(self):
        # Saves a record. Run checkexists before to see that the record is unique if that is needed
        fields=self.dynfields()
        sql="insert into "+self.tablename +"("+",".join(fields)+") values("+",".join('?'*len(fields)) +")"
        param=[]
        for field in fields:
            param.append(getattr(self,field))
        self.cursor.execute(sql,param)
        self.cursor.commit()
        print("Saving")