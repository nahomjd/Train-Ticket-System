# Train-Ticket-System

Relational Schema:
![image](https://user-images.githubusercontent.com/27834881/80921995-118f7f00-8d48-11ea-8443-f7b8dada1bbd.png)

Login:

![image](https://user-images.githubusercontent.com/27834881/80921759-43074b00-8d46-11ea-8635-528fa45ca8e6.png)

Narrative:

  This project will be a flask application for a Railway System. The main application for this project for passenger booking. You will also be able to check all supporting aspects that are related to a particular trip. 
  
  A passenger will be able to input information so as to be offered tickets for train rides using the flask application. There will be three types of users: customers/passengers, booking agents, and administrators. Passengers will only be able to input information about themselves and the required info to buy a ticket. Booking agents will be able to enter information for an existing customer to book them a train ride; they will also be able to see all data in order to help passengers with potential problems. Administrators are there to create, update, and delete the Trip, Train, and TrainStations as they need to.

  This project was a challenge blending python, HTML, and SQL into working seamlessly with each other. While doing this project I learned a lot about using classes to make this project successful. Passengers, Agents, and Admins all live seamlessly in this application. Admin pages can only be accessed by Admins. Agent pages only deny passengers from accessing them. There is no access checking for passenger pages. This is because there is no reason to try and keep Admins and Agents off the pages. Also, you need to be logged in to be on any page other than login.
  
   Error handling is pretty extensive in this ticket purchasing system. It is not possible to use any IDs for any tables that do not exist. Dates are also checked, a train can not arrive before it departs. When it comes to text inputs those are checked for being blank. Also, the session is checked for inactivity to log out users that are not active. Finally, there are some other minor errors checking to make sure pages work correctly throughout the application.
  
  For the most part, this flask application came together with the majority of the functionality working correctly. However, there are a few shortfalls I will highlight in advance. Update and deleting trips, trains, and Train stations for the administrator did not come to fruition. Update trip does have a page however it does not update the database correctly, though the error checking on it works correctly. So update trip does have partial functionality. Another shortfall is that when purchasing a ticket and purchase a ticket is submitted without selecting a ticket the page is reloaded. However, once reloaded tickets won’t appear due to not being able to access the original searched information. The final shortfall is if no information is found in a search a blank table is made. With more time I would implement a “Nothing found” message. 

Libraries used: Flask, Flask_sessions, pymsql, datetime, and time

Six Objects: Base, Passenger, Ticket, Train, TrainStations, and Trip
Passenger: deals with methods that are related to how a customer and user interacts with the application.
Ticket: Contains methods that generate a ticket as well as error check the inputs for the ticket information.
Train: Only has a verfyNew to check if inputs are blank.
TrainStations: has a VerfyNew that checks for blankl input and that zip code is the correct length
Trip: deals with creating outputs mostly for trips based on criteria. There is also error checking methods for the inputs that create the trip outputs.

Example of Two methods
getTrips:
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

This method merges 3 tables with an output dependent on date, destination, or/and origin. The method also works if all inputs are blank. The purpose of the method is to search all trips. This is for access to Trip Search in the Agent area. An agent can search trips based on any of the three inputs. For example, all trips where Grand Central is the Origin. They can also use all three inputs to get a more detailed/narrowed search.

checkNotUser:
def checkNotUser(self,userType,email):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE  `userType` <> %s and `PEmail` = %s;'
        tolkens = (userType,email)
        self.connect()
        #print(sql)
        #print(tolkens)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql,tolkens)
        self.data = []
        n = 0
        for row in cur:
            self.data.append(row)
            n+=1
        if n > 0:
            return True
        else:
            return False

This method is for keeping a specific type of user of pages. Its use case is for keeping Passenger users off the Agent's pages. This is because there was no reason to restrict an Admin from accessing the pages so instead we just check that they are not a Passenger because there are only three types of user and no way of making a new type without some kind of SQL injection attack.


CRUD Table:

![image](https://user-images.githubusercontent.com/27834881/80921812-a4c7b500-8d46-11ea-9613-e697659374da.png)
