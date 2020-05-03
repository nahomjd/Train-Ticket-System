
import pymysql
from baseObject import baseObject

class trainStationList(baseObject):
    def __init__(self):
        self.setupObject('TrainStations')
        
    def verifyNew(self, n=0):
        self.errorList = []
        for item in self.data[n]:
            #print(item)
            if item != self.pk:
                if len(self.data[n][item]) == 0:
                    st = str(item) + ' cannot be blank.'
                    self.errorList.append(st)
            if item == 'zipCode':
                if len(self.data[n][item]) != 5:
                    st = str(item) + ' needs to be 5 characters not ' + str(len(self.data[n][item]))
                    self.errorList.append(st)
        #print(self.errorList)    
        if len(self.errorList) > 0:
            return False
        else:
            return True
            
           
    
        
