import sqlite3 as lite
import hashlib

class UserManager(object):


    def check(self, user=None, passw=None, notes=False, comments=False, id_=None, comment="", note="", search=""):
        self.notes = notes
        self.id = id_
        self.note = note
        self.comment = comment
        self.comments = comments
        self.user = user
        self.passw = passw
        self.search = search
        self.con = None
        self.data = None
        try:
            self.con = lite.connect('app.db')

            self.cur = self.con.cursor()
            # Get users notes
            if self.notes and self.id:
                self.cur.execute("SELECT data FROM storage WHERE userid= '" + self.id + "' AND private = 'yes'")
                self.data = self.cur.fetchall()
            elif self.comments:
                self.cur.execute("SELECT data FROM storage WHERE private = 'no'")
                self.data = self.cur.fetchall()
            # Insert new comment to db
            elif self.comment and self.id:
                self.cur.execute("INSERT INTO storage(userid, private, data) VALUES (?,?,?)" ,(self.id, 'no', self.comment))
                self.con.commit()
            # Insert users note to db
            elif self.note and self.id:
                self.cur.execute("INSERT INTO storage(userid, private, data) VALUES (?,?,?)" ,(self.id, 'yes', self.note))
                self.con.commit()
            # Do search from comments
            elif self.search:
                self.cur.execute("SELECT * FROM storage WHERE data LIKE '%"+self.search+"%'")
                self.data = self.cur.fetchall()
            # Check login attempt
            else:
                self.cur.execute("SELECT * FROM user WHERE username= '" + self.user + "' AND password='" + self.passw + "'")
                self.data = self.cur.fetchone()
            if self.data:
                return self.data
        except Exception as e:
            raise e


        finally:

            if self.con:
                self.con.close()
