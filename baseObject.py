import pymysql

class baseObject:
   
    def setupObject(self, tn):
        self.data = []
        self.tempdata = {}
        self.tn = tn
        self.fnl = []
        self.pk = ''
        self.conn = None
        self.errorList = []
        self.getFields()
   
    def connect(self):
        import config
        self.conn = pymysql.connect(host=config.DB['host'], port=config.DB['port'], user=config.DB['user']\
        ,passwd=config.DB['passwd'], db=config.DB['db'], autocommit=True) #setup our credentials
    
    def getFields(self):
        sql = 'DESCRIBE `' + self.tn + '`;'
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        self.fnl = []
        for row in cur:
            self.fnl.append(row['Field'])
            if row['Extra'] == 'auto_increment' and row['Key'] == 'PRI':
                self.pk = row['Field']
                
    def add(self):
        self.data.append(self.tempdata)
    
    #def add(self, item):
        #self.data.append(item)
    
    def set(self,fn,val):
        if fn in self.fnl:
            self.tempdata[fn] = val
        else:
            print('Invalid field: ' + str(fn))
    
    def update(self,n,fn,val):
        if len(self.data) >= (n + 1) and fn in self.fnl:
            self.data[n][fn] = val
        else:
            print('Could not set value at row ' + str(n) + ' col ' + str(fn))
    
    def insert(self, n=0):
        columns = ''
        vals = ''
        tolkens = []
        for fieldname in self.fnl:
            if fieldname in self.data[n].keys():
                tolkens.append(self.data[n][fieldname])
                vals +='%s,'
                columns += '`'+ fieldname + '`,'
        vals = vals[:-1]
        columns = columns[:-1]
        sql = 'INSERT INTO `' + self.tn + '` ' + '(' + columns + ') VALUES (' + vals + ');'
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #print(sql)
        #print(tolkens)
        cur.execute(sql,tolkens)
        self.data[n][self.pk] = cur.lastrowid
    
    def delete(self, n=0):
        item = self.data.pop(n)
        self.deleteByID(item[self.pk])
        
    def deleteByID(self, id):
        sql = 'DELETE FROM `' + self.tn + '` WHERE `' + self.pk + '` = %s;'
        self.connect()
        tolkens = (id)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql,tolkens)
    
    def getByID(self,id):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `' + self.pk + '` = %s;'
        self.connect()
        tolkens = (id)
        #print(sql)
        #print(tolkens)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql,tolkens)
        self.data = []
        for row in cur:
            self.data.append(row)
            
    def getAll(self, order = None):
        sql = 'SELECT * FROM `' + self.tn  + '`;'
        if order != None:
            sql += ' ORDER BY `' + order+ '`'
        self.connect()
        #print(sql)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        self.data = []
        for row in cur:
            self.data.append(row)
    
    def getByField(self,field, value):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `' + field + '` = %s;'
        self.connect()
        tolkens = (value)
        #print(sql)
        #print(tolkens)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql,tolkens)
        self.data = []
        for row in cur:
            self.data.append(row)

    def getLikeField(self,field, value):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `' + field + '` = %s;'
        self.connect()
        tolkens = ('%' + value + '%')
        #print(sql)
        #print(tolkens)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql,tolkens)
        self.data = []
        for row in cur:
            self.data.append(row)