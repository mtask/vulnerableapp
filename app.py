from flask import Flask, render_template, redirect, url_for, request
import os
from bin.db_manager import *
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html', user="")
   
@app.route('/login', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      um = UserManager()
      user = request.form['nm']
      passw = request.form['passw']
      if um.check(user, passw):
           return render_template('index.html',user = user, tried_login=True)
      else:
           return render_template('index.html',user = "", tried_login=True)
           
   else:
      return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)