from flask_login import UserMixin

from werkzeug.security import generate_password_hash, \
     check_password_hash

# from .dbconnector import dbconnector
from .staticdata import metadatalist

class User(UserMixin,metadatalist):

    def __init__(self, username):
        self.id = username
        self.tablename='users'
        self.authenticated=False
        self.connecttodb()
        self.name=None
        self.email=None
        self.pw_hash=None
        self.userclass=0
        u=None
        try:
            self.cursor.execute("select username,fullname,email,hashedpassword,userclass from users where username =? ",self.id)
            u=self.cursor.fetchall()
            self.name=u[0][1]
            self.email=u[0][2]
            self.pw_hash=u[0][3]
            self.userclass=u[0][4]
        except IndexError:
            pass
        self.password = None
        print(self)
    
    def checkexists(self):
        sql="select count(*) from users where username=?"
        self.cursor.execute(sql,self.id)
        return(self.cursor.fetchall()[0][0])
    
    
    def search(self,partial=True):
        if self.cursor==None:
            self.connecttodb()
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
        
        sql = "select "+",".join(self.dynfields()) +" from "+self.tablename
        if len(values)>0:
            sql=sql+" where "+(" and ".join(fields))
        print(sql)
        print(values)
        self.cursor.execute(sql,values)
        set = self.cursor.fetchall()
        return(set)
    
    def set(self,name,email,password,userclass=0):
        self.name=name
        self.email=email
        self.set_password(password)
        self.userclass=userclass
    
    def reqset(self,request):
        print(request)
        self.fullname=request["fullname"]
        self.email=request["email"]
        self.set_password(request["hashedpassword"])
        userclass=str(int(request["userclass"]))
        self.userclass=(userclass)
    
    def fields(self):
        if self.cursor==None:   
            self.connecttodb()
        return(list(self.hash().keys()))
        
    
    def save(self):
        sql="insert into users values(?,?,?,?,?)"
        self.cursor.execute(sql,self.id,self.fullname,self.email,self.pw_hash,self.userclass)
    
    def is_authenticated(self):
        return(self.authenticated)
    
    def store_password(self):
        sql="update users set hashedpassword=? where username=?"
        self.cursor.execute(sql,self.pw_hash,self.id)
        self.cursor.commit()
    
    def update_password(self,oldpass,newpass):
        retval=False
        if self.check_password(oldpass):
            self.set_password(newpass)
            self.store_password()
            print(self.pw_hash)
            retval=True
        return(retval)
            
    def __repr__(self):
        return "%s/%s/%s/%s" % (self.id, self.name,self.email,self.pw_hash)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        ok=False
        if self.pw_hash==None:
            return False
        if self.pw_hash.startswith('pbkdf2:sha256:50000$'):
            return check_password_hash(self.pw_hash, password)
        else: # need a fallback until implementation is finished. 
            return self.pw_hash==password