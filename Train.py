
import pymysql
from baseObject import baseObject

class trainList(baseObject):
    def __init__(self):
        self.setupObject('Train')
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
            print(self.data[n][item])
            if item != self.pk:
                if len(str(self.data[n][item])) == 0:
                    st = str(item) + ' cannot be blank.'
                    self.errorList.append(st)    
        if len(self.errorList) > 0:
            return False
        else:
            return True
        
        
