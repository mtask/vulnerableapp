from flask import Flask, render_template, redirect, url_for, request, session
import os
from bin.db_manager import *

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/')
def index():
   if session.has_key('username'):
       return redirect(url_for('home'))
   return render_template('index.html', user="")
   
@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))


@app.route('/home/<id>')
def home_info(id):
    um = UserManager()
    user_info = um.check(id_=id, info=True)
    return render_template('home.html', user_info=user_info)



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

if __name__ == '__main__':
    app.run(debug = True)