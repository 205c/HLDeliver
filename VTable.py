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
        self.cur.execute("DROP TABLE IF EXISTS V") #check
        self.rows = rows
        self.columns = columns
        create_query = "CREATE TABLE V (V_Id INT(11) NOT NULL"
        for r in range(rows):
            for i in range(columns):
            create_query += ", V" + str(i) + " DECIMAL(10,2) NOT NULL"
        create_query += ", PRIMARY KEY (V_Id))"

        self.cur.execute(create_query)


    # data is a list of tuples (row_number (0 indexed), col entry0, col entry 1, ...)
    def loadTable(self, data):
        insert_string = "INSERT INTO V ("
        for c in range(self.columns):
            insert_string += "V" + str(c) + ", "
        insert_string + insert_string[:-2] +  ") VALUES ("
        insert_string += "%d, "
        for c in range(self.columns):
            insert_string +="%.2f, "
        insert_string = insert_string[:-1] + ")"

        self.cur.executemany(insert_string, data)
        




