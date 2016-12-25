import sqlite3 as lite
import hashlib

class UserManager(object):
    
    
    def check(self, user=None, passw=None, info=False, id_=None):
        self.info = info
        self.id = id_
        self.user = user
        self.passw = passw
        self.con = None
        try:
            self.con = lite.connect('app.db')
    
            self.cur = self.con.cursor()
            if self.info and self.id:
                self.cur.execute("SELECT * FROM userinfo WHERE userid= '" + self.id + "'")
            else:
                self.cur.execute("SELECT * FROM user WHERE username= '" + self.user + "' AND password='" + self.passw + "'")
    
            self.data = self.cur.fetchone()
            print str(self.data)	
            if self.data:
                return self.data
        except Exception as e:
            print "Error %s:" % e.args[0]
           
    
        finally:
    
            if self.con:
                self.con.close()