'''
In this assignment you will create a console app which stores a list of customers.  
Each customer will have the following attributes:
fname
lname
email
password
subscribed

The app should allow the user to 
Enter new customers
Remove existing customers
Update (change) a customer's attribute
Print all customers
Save / load customer list from the file 'customers.json'
In class: create and test a class definition for a customer.
'''
#INSERT INTO `customers` ('fname', 'lname', 'email', 'password', 'subscribed') VALUES ('Testguy', 'test', 'b@b.com', '1234', 'True')
import pymysql
from baseObject import baseObject

class passengerList(baseObject):
    def __init__(self):
        self.setupObject('passenger')
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
        if '@' not in self.data[n]['email'] or '.' not in self.data[n]['email']:
            self.errorList.append("Email input not valid, missing an '@' or '.'.")
        if self.data[n]['subscribed'] != 'True' and self.data[n]['subscribed'] != 'False':
            self.errorList.append('Subscribed needs to be True or False.')
        if len(self.data[n]['password']) <= 4:
            self.errorList.append('Password is too short, needs to be greater than 4 characters.')
        #print(self.errorList)    
        if len(self.errorList) > 0:
            return False
        else:
            return True
    
    def tryLogin(self,email,pw):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE ` `email` = %s and `password` = %s;'
        tolkens = (email,pw)
        self.connect()
        #print(sql)
        #print(tolkens)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql,tolkens)
        self.data = []
        for row in cur:
            self.data.append(row)
            n+=1
        if n > 0:
            return True
        else:
            return False
