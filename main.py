from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 
from flask_session import Session
import pymysql 
import json
import time
from Passenger import passengerList
   
app = Flask(__name__,static_url_path='')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

'''
=====================
Main functions Start
=====================
'''

@app.route('/set')
def set():
    session['time'] = time.time()
    return 'set'

@app.route('/get')
def get():
    return str(session['time'])
    
@app.route('/')
def home():
    return render_template('index.html', title='index', msg='Welcome Please Login or create a account!')

'''
=====================
Main functions End
=====================
'''    

'''
===================================
Passenger and Login Functions Start
===================================
'''

@app.route('/login', methods = ['GET', 'POST'])
def login():
    print('was called login')
    if request.form.get('PEmail') is not None and request.form.get('Ppassword') is not None:
        p = passengerList()
        if p.tryLogin(request.form.get('PEmail'), request.form.get('Ppassword')):
            print('login ok')
            session['user'] = p.data[0]
            session['active'] = time.time()
            return redirect('main')
        else:
            print('login failed')
            return render_template('Login.html',title='login', msg ='Incorrect email or password.')
                    
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
        
@app.route('/main')
def main():
    if checkSession() == False: 
        return redirect('login')
    userinfo = 'Hello, ' + session['user']['PFirstName']
    return render_template('main.html', title='Main menu',msg = userinfo)  

@app.route('/createaccount',methods = ['GET', 'POST'])
def createaccount():

    if request.form.get('PFirstName') is None:
        p = passengerList()
        p.set('PFirstName','')
        p.set('PLastName','')
        p.set('PEmail','')
        p.set('Ppassword','')
        p.add()
        return render_template('createaccount.html', title='New Account',  passenger=p.data[0]) 
    else:
        p = passengerList()
        p.set('PFirstName',request.form.get('PFirstName'))
        p.set('PLastName',request.form.get('PLastName'))
        p.set('PEmail',request.form.get('PEmail'))
        p.set('Ppassword',request.form.get('Ppassword'))
        p.add()
        if p.verifyNew():
            p.insert()
            #print(p.data)
            return render_template('login.html', title='Account Saved Please Login Now',  passenger=p.data[0])
        else:
            return render_template('createaccount.html', title='Account Not Saved',  passenger=p.data[0],msg=p.errorList)



'''
===================================
Passenger and Login Functions End
===================================
'''
       
if __name__ == '__main__':
   app.secret_key = '1234'
   app.run(host='127.0.0.1',debug=True)
   