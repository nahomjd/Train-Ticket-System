
import pymysql
from baseObject import baseObject

class ticketList(baseObject):
    def __init__(self):
        self.setupObject('Ticket')
        '''
        self.data = []
        self.tempdata = {}
        self.tn = 'customers'
        self.fnl = ['fname','lname','email','password','subscribed']
        self.pk = 'id'
        self.conn = None
        self.errorList = []
        '''    
    def verifyNew(self, n=0):
        self.errorList = []
        for item in self.data[n]:
            print(item)
            if item != self.pk:
                if len(self.data[n][item]) == 0:
                    st = str(item) + ' cannot be blank.'
                    self.errorList.append(st)    
        if '@' not in self.data[n]['PEmail'] or '.' not in self.data[n]['PEmail']:
            self.errorList.append("Email input not valid, missing an '@' or '.'.")
        if len(self.data[n]['Ppassword']) <= 4:
            self.errorList.append('Password is too short, needs to be greater than 4 characters.')
        #print(self.errorList)    
        if len(self.errorList) > 0:
            return False
        else:
            return True
    
    '''
    SELECT ticket.ticketID, ticket.seatType, ticket.price, ticket.tripID, ticket.PID, delayedDepartDateTime, delayedArrivalDateTime, numOfGPassengers, numOfBPassengers, numOfFPassengers, departDateTime, arrivalDateTime, delayedStatus, Origin, Destination, trip.trainID, t.stationName, t.stationID, t.Municipality, t.zipCode, t.StateOrProvince, s.stationName AS DstationName, s.stationID AS DstationID, s.Municipality AS DMunicipality, s.zipCode AS DzipCode, s.StateOrProvince AS DStateOrProvince
FROM Ticket ticket, TrainStations t, TrainStations s, Trip trip
WHERE ticket.PID = %s
AND trip.tripID = ticket.tripID
AND trip.Origin = t.stationID
AND trip.Destination = s.stationID
'''

    def getPast(self, PID):
        select = '''ticket.ticketID, ticket.seatType, ticket.price, ticket.tripID, ticket.PID, delayedDepartDateTime, \
        delayedArrivalDateTime, numOfGPassengers, numOfBPassengers, numOfFPassengers, departDateTime, arrivalDateTime, \
        delayedStatus, Origin, Destination, trip.trainID, t.stationName, t.stationID, t.Municipality, t.zipCode, \
        t.StateOrProvince, s.stationName AS DstationName, s.stationID AS DstationID, s.Municipality AS DMunicipality, \
        s.zipCode AS DzipCode, s.StateOrProvince AS DStateOrProvince'''
        sql = 'SELECT ' + select + ' FROM `' + self.tn  + '` ticket' + ',`TrainStations` t, `TrainStations` s, `Trip` trip'+\
        ' WHERE ticket.PID = %s AND trip.Origin = t.stationID' +\
        ' AND trip.tripID = ticket.tripID AND trip.Destination = s.stationID '
        #print(len(Origin))
        self.connect()
        #print(sql)
        tolkens = PID
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, tolkens)
        self.data = []
        for row in cur:
            #print(row)
            self.data.append(row)
          
    
        
    

        
