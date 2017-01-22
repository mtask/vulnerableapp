from flask import Flask, render_template, redirect, url_for, request, session, render_template_string

import os
from bin.db_manager import *

app = Flask(__name__)
app.secret_key = 'any random string'
db = DbManager()


@app.route('/')
def index():
   comments = db.check(comments=True)
   if session.has_key('username'):
       return redirect(url_for('home'))
   if not comments:
       comments = []
   # Show only 5 newest comments to user
   if len(comments) > 5:
       comments = comments[5:]
   return render_template('index.html', user="", comments=comments)

@app.route('/search', methods = ['POST', 'GET'])
def search():
    # Search content with searchterm provided by user
    search = request.args['term']
    if not search:
        return render_template('search.html', res="")
    res = db.check(search=search)
    if not res:
        res = "Nothing found with: "+search
    print search
    return render_template('search.html', res=res)

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))


@app.route('/home/id/<id>')
def home_notes(id):
    # Request for users private notes
    user_notes = db.check(id_=id, notes=True)
    if session.has_key('username'):
        return render_template('home.html', user_notes=user_notes)
    else:
        return redirect(url_for('index'))

@app.route('/register')
def register():
     template = '''<p>Registaration is not available at the moment</p>'''
     return render_template_string(template)

@app.route('/home')
def home():
   if request.form:
       print request.form['amount']
   if session.has_key('username'):
       comments = db.check(comments=True)
       if not comments:
           # db.check returns None type if nothing found.
           # comments is then declared here to empty list so it will not throw exception in template.
           comments = []
       if len(comments) > 5:
           # Show only 5 newest comments to user
           comments = comments[5:]
       return render_template('home.html', comments=comments)
   else:
       return redirect(url_for('index'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      passw = request.form['passw']
      userdata = db.check(user, passw)
      if userdata:
           session['username'] = userdata[1]
           session['uuid'] = userdata[0]
           return redirect(url_for('home'))
      else:
           return render_template('index.html',user = user, tried_login=True)

   else:
      return redirect(url_for('index'))

@app.route('/sendata', methods = ['POST', 'GET'])
def sendata():
    private = False
    if request.method == 'POST':
        note = request.form['note']
    else:
        note = request.args['note']
    print note
    try:
        private = request.args['private']
    except Exception:
        private = False

    if private:
        db.check(id_=session['uuid'], note=note)
    else:
        db.check(id_=session['uuid'], comment=note)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug = True)
