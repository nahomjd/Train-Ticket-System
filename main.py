from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 
from flask_session import Session
import pymysql 
import json
import time
from customer import customerList
   
app = Flask(__name__,static_url_path='')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route('/set')
def set():
    session['time'] = time.time()
    return 'set'

@app.route('/get')
def get():
    return str(session['time'])
    
@app.route('/')
def home():
    return render_template('test.html', title='Test', msg='Welcome!')
    
@app.route('/login', methods = ['Post'])
def login():
    if request.form.get('email') is not None and request.form.get('password') is not None:
        c = customerList()
        if c.tryLogin(request.form.get('email'), request.form.get('password')):
            print('login ok')
            session['user'] = c.data[0]
            session['active'] = time.time()
            return redirect('main')
        else:
            print('login failed')
            return render_template('login.html',title='login', msg ='Incorrect username or password.')
            
        return''
    else:
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('Login.html',title='login', msg ='Type your email and password to continue.')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    del session['user']
    del session['active']
    return render_template('Login.html',title='login', msg ='You are logged out')
    
def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        if timeSinceAct > 15:
            session['msg'] = 'You have timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False
    
if __name__ == '__main__':
   app.secret_key = '1234'
   app.run(host='127.0.0.1',debug=True)
   