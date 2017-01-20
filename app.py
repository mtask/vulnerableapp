from flask import Flask, render_template, redirect, url_for, request, session, render_template_string

import os
from bin.db_manager import *

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/')
def index():
   if session.has_key('username'):
       return redirect(url_for('home'))
   return render_template('index.html', user="")

@app.route('/search')
def search():
    # Do some content search here
    search = request.args.get('srchterm')
    res = ""
    print search
    template='search.search'
    if not res:
        res = search
    return render_template('search.html', res="<script>alert(1)</script>")

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))


@app.route('/home/id/<id>')
def home_notes(id):
    um = UserManager()
    user_notes = um.check(id_=id, notes=True)
    if session.has_key('username'):
        return render_template('home.html', user_notes=user_notes)
    else:
        return redirect(url_for('index'))

@app.route('/home')
def home():
   if request.form:
       print request.form['amount']
   if session.has_key('username'):
       return render_template('home.html')
   else:
       return redirect(url_for('index'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      um = UserManager()
      user = request.form['nm']
      passw = request.form['passw']
      userdata = um.check(user, passw)
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

    um = UserManager()
    if private:
        um.check(id_=session['uuid'], note=note)
    else:
        um.check(id_=session['uuid'], comment=note)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug = True)
