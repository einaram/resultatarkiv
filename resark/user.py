from flask_login import UserMixin

from werkzeug.security import generate_password_hash, \
     check_password_hash

from .dbconnector import dbconnector

class User(UserMixin,dbconnector):

    def __init__(self, username):
        self.id = username
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
    
    def is_authenticated(self):
        return(self.authenticated)
    
    def __repr__(self):
        return "%s/%s/%s/%s" % (self.id, self.name,self.email,self.pw_hash)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        ok=False
        if self.pw_hash==None:
            return False
        if self.pw_hash.startswith('sha'):
            return check_password_hash(self.pw_hash, password)
        else: # need a fallback until implementation is finished. 
            return self.pw_hash==password