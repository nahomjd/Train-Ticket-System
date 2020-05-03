
import pymysql
from baseObject import baseObject
from datetime import date, datetime as dt

class tripList(baseObject):
    def __init__(self):
        self.setupObject('Trip')
   
    def verifyNew(self, n=0):
        self.errorList = []
        for item in self.data[n]:
            print(item)
            if item != self.pk:
                if len(str(self.data[n][item])) == 0:
                    st = str(item) + ' cannot be blank.'
                    self.errorList.append(st)
        if len(self.errorList) > 0:
            return False
        else:
            return True
    
    def checkPurchase(self, selectedDate,User):
        self.errorList = []

        if User == '':
            self.errorList.append('No user selected.')
        if selectedDate == '':
            self.errorList.append('No date selected.')
            return False
        
        sql = 'select * from Passenger where PID = %s;'
        self.connect()
        tolken = User
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tolken)
        passenger = []
        for row in cur:
            passenger.append(row)
        if len(passenger) > 0:
            test = 1
            #do nothing
        else:
            self.errorList.append('User does not exist.')

        selected = dt.strptime(selectedDate,"%Y-%m-%d")
        today = dt.strptime(str(date.today()),"%Y-%m-%d")
        print(selected)
        print(today)
        if  selected < today:
            #print('Past')
            self.errorList.append('Date selected is in the past.')
        if len(self.errorList) > 0:
            #print('False')
            return False
        else:
            #print('True')
            #print(self.errorList)
            return True
        
    def getStations(self):
        sql = 'select stationName from TrainStations;'
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        stations = []
        for row in cur:
            stations.append(row['stationName'])
        return stations
    
    def getTrain(self):
        sql = 'select * from Train;'
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        train = []
        for row in cur:
            print(row)
            
    def CheckTrainID(self, TrainID):
        self.errorList = []
        sql = 'select * from Train where trainID = %s;'
        self.connect()
        tolken = TrainID
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tolken)
        train = []
        for row in cur:
            train.append(row)
        if len(train) > 0:
            return True
        else:
            self.errorList.append('Train Does Not Exist')
            return False
           
    def CheckTripID(self, TripID):
        self.errorList = []
        sql = 'select * from Trip where tripID = %s;'
        self.connect()
        tolken = TripID
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tolken)
        trip = []
        for row in cur:
            trip.append(row)
        if len(trip) > 0:
            return True
        else:
            self.errorList.append('Trip Does Not Exist')
            return False
            
    def verifyPossibleTrip(self, n=0):
        self.errorList = []
        #print(self.data[n])
        try:
            if self.data[n]['departDateTime'] > self.data[n]['arrivalDateTime']:
                st = 'Arrival can not be before depart!'
                self.errorList.append(st)
        except:
            if self.data[n]['delayedDepartDateTime'] > self.data[n]['delayedArrivalDateTime']:
                st = 'Arrival can not be before depart!'
                self.errorList.append(st)
        try:
            if self.data[n]['Origin'] == self.data[n]['Destination']:
                st = 'Origin and destination can not be the same.'
                self.errorList.append(st)
        except:
            test = 1
            #do nothing
        if len(self.errorList) > 0:
            return False
        else: 
            return True
    
    def getAll(self, order = None):
        select = '''tripID, delayedDepartDateTime, delayedArrivalDateTime, numOfGPassengers, numOfBPassengers, numOfFPassengers, departDateTime, arrivalDateTime, delayedStatus, Origin, Destination, trainID, t.stationName\
        , t.stationID, t.Municipality, t.zipCode, t.StateOrProvince, s.stationName as DstationName, s.stationID as DstationID, s.Municipality as DMunicipality, s.zipCode as DzipCode, s.StateOrProvince as DStateOrProvince'''
        sql = 'SELECT ' + select + ' FROM `' + self.tn  + '`' + ',`TrainStations` t, `TrainStations` s' +\
        ' WHERE DATE ( departDateTime ) = %s AND t.stationID = Origin AND s.stationID = Destination;'
        if order != None:
            sql += ' ORDER BY `' + order+ '`'
        tolken = date.today()    
        self.connect()
        print(sql)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tolken)
        self.data = []
        for row in cur:
            #print(row)
            self.data.append(row)
    
            
    #SELECT * FROM Trip, TrainStations t, TrainStations s WHERE DATE ( departDateTime ) = 2020-04-29 AND t.stationID = Origin AND s.stationID = Destination;
    def getTrips(self, Destination, Date, Origin):
        select = '''tripID, delayedDepartDateTime, delayedArrivalDateTime, numOfGPassengers, numOfBPassengers, numOfFPassengers, departDateTime, arrivalDateTime, delayedStatus, Origin, Destination, trip.trainID, t.stationName\
        , t.stationID, t.Municipality, t.zipCode, t.StateOrProvince, s.stationName as DstationName, s.stationID as DstationID, s.Municipality as DMunicipality, s.zipCode as DzipCode, s.StateOrProvince as DStateOrProvince\
        ,tr.trainID, tr.numberOfFirstClassSeats, tr.numberOfBusinessClassSeats, tr.numberOfGeneralSeats, tr.trainType, tr.company'''
        sql = 'SELECT ' + select + ' FROM `' + self.tn  + '` trip' + ',`TrainStations` t, `TrainStations` s, `Train` tr' +\
        ' WHERE t.stationID = Origin AND s.stationID = Destination' +\
        ' AND trip.trainID = tr.trainID'
        #print(len(Origin))
        tolkens = []
        if len(Date) > 0:
            sql += ' And DATE ( departDateTime ) = %s'
            tolkens.append(Date)
        '''
        if len(Origin) > 0 and len(Destination) > 0:
            sql += ' AND t.stationID = %s'
            sql += ' AND s.stationID = %s'
            tolkens = [Date, Origin, Destination]
        '''
        if len(Origin) > 0:
            sql += ' AND t.stationID = %s'
            tolkens.append(Origin)
        if len(Destination) > 0:
            sql += ' AND s.stationID = %s'
            tolkens.append(Destination)
        sql += ';'

        
        self.connect()
        print(sql)
        print(tolkens)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tolkens)
        self.data = []
        for row in cur:
            #print(row)
            self.data.append(row)
            
    def updatePassengers(self, type, tripID):
        sql = 'UPDATE `' + self.tn + '` SET ' + type +'='+ type +'+1 WHERE tripID = %s;'
        #sql = 'UPDATE `' + self.tn + '` SET %s=%s+1 WHERE tripID = %s;' version doesn't work
        tolken = tripID
        self.connect()
        #print(sql)
        #print(tolkens)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tolken)
        
        
        
    
    
        
