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
   return render_template('index.html', user="", comments=comments)

@app.route('/search', methods = ['POST', 'GET'])
def search():
    # Do some content search here
    search = request.args['term']
    res = db.check(search=search)
    print res
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
    user_notes = db.check(id_=id, notes=True)
    comments = db.check(comments=True)
    if session.has_key('username'):
        print user_notes
        return render_template('home.html', user_notes=user_notes)
    else:
        return redirect(url_for('index'))

@app.route('/home')
def home():
   if request.form:
       print request.form['amount']
   if session.has_key('username'):
       comments = db.check(comments=True)
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

@app.route('/sendata')
def sendata():
    private = False
    note = request.args['note']
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
