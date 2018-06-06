
from .dbconnector import *

class searchdata(dbconnector):

    def listdata(self,table):
        sql = "select id,name from "+table+" order by name"
        print(sql)
        self.cursor.execute(sql)
        table=self.cursor.fetchall()
        print(table)
        return(table)
        
        


    def __init__(self):
        self.connecttodb()        

        
    
        
    def search(self):
        True
    

    
