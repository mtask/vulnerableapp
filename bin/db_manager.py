import sqlite3 as lite
import hashlib

class UserManager(object):

    
    
    def check(self, user, passw):
        self.con = None
        try:
            self.con = lite.connect('app.db')
    
            self.cur = self.con.cursor()    
            self.cur.execute("SELECT * FROM user WHERE username= '" + user + "' AND password='" + passw + "'")
    
            self.data = self.cur.fetchone()
            print self.data	
            if self.data:
                return self.data
        except Exception as e:
            print "Error %s:" % e.args[0]
           
    
        finally:
    
            if self.con:
                self.con.close()