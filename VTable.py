import MySQLdb

class VTable(object):

    def __init__(self, host, user, pwd, db):
        self.db = MySQLdb.connect(host=host,
                             user=user,
                             passwd=pwd,
                             db=db)

        self.cur = self.db.cursor() 
        self.rows = 25
        self.columns = 47
    

    def createTable(self, rows, columns):
        #self.cur.execute("DROP TABLE IF EXISTS V") #check
        self.rows = rows
        self.columns = columns
        create_query = "CREATE TABLE V (V_Id INT(11) NOT NULL"
        #for r in range(rows):
        for i in range(columns):
            create_query += ", V" + str(i) + " DECIMAL(10,2) NOT NULL"
        create_query += ", PRIMARY KEY (V_Id))"
        #create_query += ", PRIMARY KEY (IV_MB_ID), FOREIGN KEY (IV_MB_ID) references Members(MB_Id)) ENGINE=INNODB"
        print create_query
        self.cur.execute(create_query)


    # data is a list of tuples (row_number (0 indexed), col entry0, col entry 1, ...)
    def loadTable(self, data):
        for c in range(self.columns):
            d = data[c]
            self.cur.execute('INSERT INTO V VALUES ' + str(d))
        self.db.commit()
        


    # makes a default V table
    def makeTestData(self):
        data = [] 
        for i in range(self.rows):
            d = (i,)*(self.columns+1)
            self.cur.execute('INSERT INTO V VALUES ' + str(d))
 
        self.db.commit()
        #self.loadTable(data)
