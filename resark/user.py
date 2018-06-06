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
        u=None
        try:
            self.cursor.execute("select username,fullname,email,hashedpassword,userclass from users where username =? ",self.id)
            u=self.cursor.fetchall()
            self.name=u[0][1]
            self.email=u[0][2]
            self.pw_hash=u[0][3]
            self.userclass=u[0][4]
            self.authenticated= len(u)==1
        except pyodbc.DataError:
            print(self.id)
            pass
        except IndexError:
            self.authenticated=False
        self.password = None
        print(self)
    
    def is_authenticated(self):
        return(self.authenticated)
    
    def __repr__(self):
        return "%s/%s/%s/%s" % (self.id, self.name,self.email,self.pw_hash)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)