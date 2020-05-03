from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 
from flask_session import Session
import pymysql 
import json
import time
from Passenger import passengerList
from TrainStations import trainStationList
from Train import trainList
from Trip import tripList
from Ticket import ticketList
from datetime import date

today = date.today()
   
app = Flask(__name__,static_url_path='')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

'''
=====================
default functions Start
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
default functions End
=====================
'''    

'''
===================================
Login Functions Start
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

@app.route('/createaccount',methods = ['GET', 'POST'])
def createaccount():

    if request.form.get('PFirstName') is None:
        p = passengerList()
        p.set('PFirstName','')
        p.set('PLastName','')
        p.set('PEmail','')
        p.set('Ppassword','')
        p.set('userType','')
        p.add()
        return render_template('createaccount.html', title='New Account',  passenger=p.data[0]) 
    else:
        p = passengerList()
        p.set('PFirstName',request.form.get('PFirstName'))
        p.set('PLastName',request.form.get('PLastName'))
        p.set('PEmail',request.form.get('PEmail'))
        p.set('Ppassword',request.form.get('Ppassword'))
        p.set('userType','Passenger')
        p.add()
        if p.verifyNew():
            p.insert()
            #print(p.data)
            return render_template('login.html', title='Account Saved Please Login Now',  passenger=p.data[0])
        else:
            return render_template('createaccount.html', title='Account Not Saved',  passenger=p.data[0],msg=p.errorList)

@app.route('/main')
def main():
    p = passengerList()
    if checkSession() == False: 
        return redirect('login')
    if p.checkUser('Admin',session['user']['PEmail']):
        userinfo = 'Admin Page'
        print('Admin Page')
        return render_template('admin.html', title='Main menu',msg = userinfo) 
    elif p.checkUser('Agent',session['user']['PEmail']):
        userinfo = 'Agent Page'
        return render_template('agent.html', title='Main menu',msg = userinfo)  
    else:
        userinfo = 'Hello, ' + session['user']['PFirstName']
        return render_template('main.html', title='Main menu',msg = userinfo)  

'''
===================================
Login Functions End
===================================
'''

'''
===================================
Admin Functions Start
===================================
'''
@app.route('/addstation',methods = ['GET', 'POST'])
def addstation():
    p = passengerList()
    if checkSession() == False: 
        return redirect('login')
    if p.checkUser('Admin',session['user']['PEmail']):
        if request.form.get('stationName') is None:
            t = trainStationList()
            t.set('stationName','')
            t.set('Municipality','')
            t.set('zipCode','')
            t.set('StateOrProvince','')
            t.add()
            return render_template('addstation.html', title='New Station',  trainstation=t.data[0], msg=t.errorList) 
        else:
            t = trainStationList()
            t.set('stationName',request.form.get('stationName'))
            t.set('Municipality',request.form.get('Municipality'))
            t.set('zipCode',request.form.get('zipCode'))
            t.set('StateOrProvince',request.form.get('StateOrProvince'))
            t.add()
            if t.verifyNew():
                t.insert()
                return render_template('admin.html', title='Station Saved!',  trainstation=t.data[0], msg=t.errorList)
            else:
                return render_template('addstation.html', title='Station Not Saved!',  trainstation=t.data[0], msg=t.errorList)
    else:
        return redirect('main')
        
#not working yet
@app.route('/addtrain',methods = ['GET', 'POST'])
def addtrain():
    p = passengerList()
    if checkSession() == False: 
        return redirect('login')
    if p.checkUser('Admin',session['user']['PEmail']):
        if request.form.get('company') is None:
            t = trainList()
            t.set('numberOfFirstClassSeats','')
            t.set('numberOfBusinessClassSeats','')
            t.set('numberOfGeneralSeats','')
            t.set('trainType','')
            t.set('company','')
            t.add()
            return render_template('addtrain.html', title='New Train',  train=t.data[0], msg = ['company is blank'])
        else:
            t = trainList()
            t.set('numberOfFirstClassSeats',request.form.get('numberOfFirstClassSeats'))
            t.set('numberOfBusinessClassSeats',request.form.get('numberOfBusinessClassSeats'))
            t.set('numberOfGeneralSeats',request.form.get('numberOfGeneralSeats'))
            t.set('trainType',request.form.get('trainType'))
            t.set('company',request.form.get('company'))
            t.add()
            if t.verifyNew():
                print(t.data[0])
                t.insert()
                return render_template('admin.html', title='Train Saved!',  train=t.data[0], msg=t.errorList)
            else:
                print(t.data[0])
                return render_template('addtrain.html', title='Train Not Saved!',  train=t.data[0], msg=t.errorList)
    else:
        return redirect('main')
        
@app.route('/adduser',methods = ['GET', 'POST'])
def adduser():
    p = passengerList()
    if checkSession() == False: 
        return redirect('login')
    if p.checkUser('Admin',session['user']['PEmail']):
        if request.form.get('PFirstName') is None:
            p = passengerList()
            p.set('PFirstName','')
            p.set('PLastName','')
            p.set('PEmail','')
            p.set('Ppassword','')
            p.set('userType','')
            p.add()
            return render_template('adduser.html', title='New Account',  passenger=p.data[0]) 
        else:
            p = passengerList()
            p.set('PFirstName',request.form.get('PFirstName'))
            p.set('PLastName',request.form.get('PLastName'))
            p.set('PEmail',request.form.get('PEmail'))
            p.set('Ppassword',request.form.get('Ppassword'))
            p.set('userType',request.form.get('userType'))
            p.add()
            if p.verifyNew():
                p.insert()
                #print(p.data)
                return render_template('admin.html', title='Account Created',  passenger=p.data[0])
            else:
                return render_template('createaccount.html', title='Account Not Saved',  passenger=p.data[0],msg=p.errorList)
    else:
        return redirect('main')
#Need add and update trip still
@app.route('/addtrip',methods = ['GET', 'POST'])
def addtrip():
    
    p = passengerList()
    if checkSession() == False: 
        return redirect('login')
    if p.checkUser('Admin',session['user']['PEmail']):
        if request.form.get('Origin') is None:
            t = tripList()
            t.set('Origin','')
            t.set('Destination','')
            t.set('delayedDepartDateTime','')
            t.set('delayedArrivalDateTime','')
            t.set('departDateTime','')
            t.set('departDateTime','')
            t.set('trainID','')
            t.set('numOfGPassengers','')
            t.set('numOfBPassengers','')
            t.set('numOfFPassengers','')
            t.set('delayedStatus','')
            t.add()
            s = trainStationList()
            s.getAll()
            #stations = t.getStations()
            t.getTrain()
            #print(stations)
            return render_template('addtrip.html', title='New Trip',  train=t.data[0], stations = s.data)
        else:
            t = tripList()
            t.set('Origin',request.form['Origin'])
            t.set('Destination',request.form['Destination'])
            t.set('departDateTime',request.form.get('departDate') + ' ' + request.form.get('departTime'))
            t.set('arrivalDateTime',request.form.get('arrivalDate') + ' ' + request.form.get('arrivalTime'))
            t.set('trainID',request.form.get('trainID'))
            t.set('numOfGPassengers',0)
            t.set('numOfBPassengers',0)
            t.set('numOfFPassengers',0)
            t.set('delayedStatus','On Time')
            t.add()
            s = trainStationList()
            s.getAll()
            if t.verifyNew():
                if t.verifyPossibleTrip() and t.CheckTrainID(request.form.get('trainID')):
                    #print(t.data[0])
                    t.insert()
                    return render_template('admin.html', title='Trip Saved!',  train=t.data[0])
                else:
                    #print(t.data[0])
                    return render_template('addtrip.html', title='Trip Not Saved!',  train=t.data[0], msg=t.errorList, stations = s.data)
            else:
                #print(t.data[0])
                return render_template('addtrip.html', title='Trip Not Saved!',  train=t.data[0], msg=t.errorList, stations = s.data)
    else:
        return redirect('main')

@app.route('/updatetrip',methods = ['GET', 'POST'])
def updatetrip():
    p = passengerList()
    if checkSession() == False: 
        return redirect('login')
    if p.checkUser('Admin',session['user']['PEmail']):
        if request.form.get('delayedStatus') is None:
            t = tripList()
            t.set('Origin','')
            t.set('Destination','')
            t.set('delayedDepartDateTime','')
            t.set('delayedArrivalDateTime','')
            t.set('departDateTime','')
            t.set('departDateTime','')
            t.set('trainID','')
            t.set('delayedStatus','')
            t.add()
            return render_template('updatetrip.html', title='New Trip',  train=t.data[0])
        else:
            t = tripList()
            t.set('tripID', request.form.get('tripID'))
            t.set('delayedDepartDateTime',request.form.get('departDate') + ' ' + request.form.get('departTime'))
            t.set('delayedArrivalDateTime',request.form.get('arrivalDate') + ' ' + request.form.get('arrivalTime'))
            t.set('trainID',request.form.get('trainID'))
            t.set('delayedStatus',request.form.get('delayedStatus'))
            t.update(0,'tripID', request.form.get('tripID'))
            t.update(0,'delayedDepartDateTime',request.form.get('departDate') + ' ' + request.form.get('departTime'))
            t.update(0,'delayedArrivalDateTime',request.form.get('arrivalDate') + ' ' + request.form.get('arrivalTime'))
            t.update(0,'trainID',request.form.get('trainID'))
            t.update(0,'delayedStatus',request.form.get('delayedStatus'))
            t.add()
            if t.verifyNew():
                if t.verifyPossibleTrip() and t.CheckTrainID(request.form.get('trainID')) and t.CheckTripID(request.form.get('tripID')):
                    #print(t.data[0])
                    t.updateSQL()
                    return render_template('admin.html', title='Trip Saved!',  train=t.data[0])
                else:
                    #print(t.data[0])
                    return render_template('updatetrip.html', title='Trip Not Saved!',  train=t.data[0], msg=t.errorList)
            else:
                print(t.data[0])
                #print('hi')
                return render_template('updatetrip.html', title='Trip Not Saved!',  train=t.data[0], msg=t.errorList)
    else:
        return redirect('main')
'''
==================================
Admin Functions End
==================================
'''

'''
===================================
Passenger Functions Start
===================================
'''
@app.route('/purchaseticket',methods = ['GET','POST'])
def purchaseTicket():
    if checkSession() == False: 
        return redirect('login')
    if request.form.get('Destination') is None:
        #print('hi')
        t = tripList()
        stations = t.getStations()
        date = request.form.get('departDate')
        Origin = request.form.get('Origin')
        Destination = request.form.get('Destination')
        #print(date)
        #print(Origin)
        #print(Destination)
        s = trainStationList()
        s.getAll()
        return render_template('purchaseticket.html', title="Search for Ticket", stations = s.data)
    else:
        t = tripList()
        stations = t.getStations()
        date = request.form['departDate']
        Origin = request.form['Origin']
        Destination = request.form['Destination']
        t.getTrips(Destination, date, Origin)
        
        #print(date)
        #print(Origin)
        #print(Destination)
        #return info for search write SQL function in trips
        s = trainStationList()
        s.getAll()
        if not t.checkPurchase(date,session['user']['PID']):
            return render_template('purchaseticket.html', title="Search for Ticket", stations = s.data, msg=t.errorList)
        else:
            return render_template('search.html', title="Search for Ticket", trips = t.data)
        
@app.route('/search', methods = ['GET','POST'])
def buyTicket():
    if checkSession() == False: 
        return redirect('login')
    #Need to get tripID, seattype, price, and PID
    if request.form.get('tripInfo') is None:
        return render_template('search.html', title="No Ticket Selected")
    else:
        tripInfo=request.form.get('tripInfo')
        splitTripInfo=tripInfo.split(',')
        t = ticketList()
        tr = tripList()
        print(splitTripInfo)
        t.set('seatType', splitTripInfo[1])
        t.set('price', splitTripInfo[2])
        t.set('PID', session['user']['PID'])
        t.set('tripID', splitTripInfo[0])
        t.add()
        t.insert()
        if splitTripInfo[1] == 'GeneralTicket':
            tr.updatePassengers('numOfGPassengers', splitTripInfo[0])
        elif splitTripInfo[1] == 'BusinessTicket':
            tr.updatePassengers('numOfBPassengers', splitTripInfo[0])
        elif splitTripInfo[1] == 'FirstClassTicket':
            tr.updatePassengers('numOfFPassengers', splitTripInfo[0])
            
        return render_template('main.html', title="Ticket Purchased")
       
        
@app.route('/editprofile', methods = ['GET','POST'])
def editProfile():
    if checkSession() == False: 
        return redirect('login')
    #will show current email, password, first name, last name, and usertype
    #will be able to edit email, password, first name, and last name
    
    #print(request.form['edit2'])
    #print(request.form.get('edit2'))
    if request.form.get('edit2') is None:
        #print('test')
        #print(request.form.get('edit'))
        return render_template('editprofile.html', title="Profile", session=session['user'])
    elif request.form.get('edit') is not None:
        p = passengerList()
        p.getByID(session['user']['PID'])
        #print(session['user'])
        #print(p.getByField('PID',session['user']['PID']))
        fname= request.form.get('firstname')
        lname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        if fname == '' and lname == '' and email == '' and password == '':
            return render_template('editprofile.html', title="Profile", session=session['user'], msg='All fields were blank')
        
        if fname == '':
            p.update(0,'PFirstName',session['user']['PFirstName'])
        else:
            p.update(0,'PFirstName',fname)
        if lname == '':
            p.update(0,'PLastName',session['user']['PLastName'])
        else:
            p.update(0,'PLastName',lname)
        if email == '':
            p.update(0,'PEmail',session['user']['PEmail'])
        else:
            p.update(0,'PEmail',email)
        if password == '':
            p.update(0,'Ppassword',session['user']['Ppassword'])
        else:
            p.update(0,'Ppassword',password)
        
        if p.verifyNew():
            p.updateSQL()
            return render_template('main.html', title="Profile Changed",session=session['user'])
        else:
            return render_template('editprofile.html', title="Profile", session=session['user'], msg=t.errorList)
        '''
        print(fname)
        print(lname)
        print(email)
        print(password)
        print(session)
        '''
        
        return render_template('main.html', title="Profile Changed",session=session['user'])
    else:
        return render_template('main.html', title="No Info Changed",session=session['user'])
   
@app.route('/pastrides', methods = ['GET','POST'])
def pastTransactions():
    if checkSession() == False: 
        return redirect('login')
    t = ticketList()
    t.getPast(session['user']['PID'])
    return render_template('pastrides.html', title="Past Transactions", transactions=t.data, session=session['user'])

'''
==================================
Passenger Functions End
==================================
'''

'''
===================================
Agent Functions Start
===================================
'''
@app.route('/purchaseticketForUser',methods = ['GET','POST'])
def purchaseticketForUser():
    if checkSession() == False: 
        return redirect('login')
    p = passengerList()
    if p.checkNotUser('Passenger',session['user']['PEmail']):
        if request.form.get('Destination') is None:
            #print('hi')
            t = tripList()
            stations = t.getStations()
            date = request.form.get('departDate')
            Origin = request.form.get('Origin')
            Destination = request.form.get('Destination')

            #print(date)
            #print(Origin)
            #print(Destination)
            s = trainStationList()
            s.getAll()
            return render_template('purchaseticketForUser.html', title="Search for Ticket", stations = s.data)
        else:
            s = trainStationList()
            s.getAll()
            t = tripList()
            stations = t.getStations()
            date = request.form['departDate']
            Origin = request.form['Origin']
            Destination = request.form['Destination']
            User = request.form['User']
            #print(date)
            if not t.checkPurchase(date,User):
                return render_template('purchaseticketForUser.html', title="Search for Ticket", stations = s.data, msg=t.errorList)
            else:
                t.getTrips(Destination, date, Origin)
                
                #print(date)
                #print(Origin)
                #print(Destination)
                #return info for search write SQL function in trips
                return render_template('searchU.html', title="Search for Ticket", trips = t.data, user = User)
    else:
        return redirect('main')
        
@app.route('/searchU', methods = ['GET','POST'])
def buyTicketU():
    if checkSession() == False: 
        return redirect('login')
    p = passengerList()
    if p.checkNotUser('Passenger',session['user']['PEmail']):
        #Need to get tripID, seattype, price, and PID
        if request.form.get('tripInfo') is None:
            return render_template('searchU.html', title="No Ticket Selected")
        else:
            tripInfo=request.form.get('tripInfo')
            splitTripInfo=tripInfo.split(',')
            t = ticketList()
            tr = tripList()
            print(splitTripInfo)
            t.set('seatType', splitTripInfo[1])
            t.set('price', splitTripInfo[2])
            t.set('PID', splitTripInfo[3])
            t.set('tripID', splitTripInfo[0])
            t.add()
            t.insert()
            if splitTripInfo[1] == 'GeneralTicket':
                tr.updatePassengers('numOfGPassengers', splitTripInfo[0])
            elif splitTripInfo[1] == 'BusinessTicket':
                tr.updatePassengers('numOfBPassengers', splitTripInfo[0])
            elif splitTripInfo[1] == 'FirstClassTicket':
                tr.updatePassengers('numOfFPassengers', splitTripInfo[0])
                
            return render_template('admin.html', title="Ticket Purchased")
    else:
        return redirect('main')

@app.route('/userinfo', methods = ['GET','POST'])
def userInfo():
    if checkSession() == False: 
        return redirect('login')
    p = passengerList()
    if p.checkNotUser('Passenger',session['user']['PEmail']):
        print(request.form.get('User'))
        if request.form.get('User') is None:
            return render_template('userInfo.html', title="Enter UserID", msg=p.errorList)
        else:
            #Does User Exist
            if p.checkExist(request.form.get('User')):
                #print('fail')
                return render_template('userInfo.html', title="Enter UserID", msg=p.errorList)
            else:
                #print('pass')
                t = ticketList()
                t.getPast(request.form.get('User'))
                return render_template('usersearch.html', title="User Info", transactions=t.data, userid = request.form.get('User'))
    else:
        return redirect('main')
        
@app.route('/tripinfo',methods = ['GET','POST'])
def tripInfo():
    if checkSession() == False: 
        return redirect('login')
    p = passengerList()
    if p.checkNotUser('Passenger',session['user']['PEmail']):
    
        if request.form.get('departDate') is None:
            #print('hi')
            t = tripList()
            stations = t.getStations()
            date = request.form.get('departDate')
            Origin = request.form.get('Origin')
            Destination = request.form.get('Destination')
            #print(date)
            #print(Origin)
            #print(Destination)
            s = trainStationList()
            s.getAll()
            return render_template('tripinfo.html', title="Search for Trips", stations = s.data)
        else:
            t = tripList()
            stations = t.getStations()
            date = request.form['departDate']
            Origin = request.form['Origin']
            Destination = request.form['Destination']
            print(date)
            print(Destination)
            t.getTrips(Destination, date, Origin)
            
            #print(date)
            #print(Origin)
            #print(Destination)
            #return info for search write SQL function in trips
            return render_template('tripsearch.html', title="Search for Trip", trips = t.data)
    else:
        return redirect('main')
        
'''
==================================
Agent Functions End
==================================
'''

'''
===================================
General Functions Start
===================================
'''
@app.route('/seetripboard',methods = ['GET','POST'])
def seetripboard():
    if checkSession() == False: 
        return redirect('login')
    t = tripList()
    t.getAll()
    #print(t.data)
    return render_template('seetripboard.html', title="Today's Trips", trips = t.data)
'''
==================================
General Functions End
==================================
'''


def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        if timeSinceAct > 500:
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
   