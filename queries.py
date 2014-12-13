import MySQLdb
import ast

'''
class represents a cluster of experiences based on members
provides functions to access expriences created or wishlisted (liked)
provide a MB_Id and an ExperienceQuery object arguments to constructor to get User associated with 
one member
'''
class User:
    def __init__(self, id, exp_qry, start_date="", interests=[]):
        self.MB_Id = id
        self.MB_InterestsRaw = interests
        self.experience_query = exp_qry
        self.start_date = start_date
    
    #returns experiences created by this member
    def get_experiences_created(self):
        self.experience_query.reset()
        if self.start_date != "":
            self.experience_query.start_date = self.start_date
        self.experience_query.initialize(EX_MB_Id=self.MB_Id)
        return self.experience_query.get_experiences();
    
    # returns experiences wishlisted by this member
    def get_experiences_wishlisted(self):
        self.experience_query.reset()
        if self.start_date != "":
            self.experience_query.start_date = self.start_date
        self.experience_query.initialize(EX_MB_Id=self.MB_Id)
        return self.experience_query.get_wishlisted_experiences(self.MB_Id)

# class to get a list of Users
class UserQuery:
    
    def __init__(self, host, user, pwd, db):
        self.db = MySQLdb.connect(host=host,
                             user=user,
                             passwd=pwd,
                             db=db)
        self.cur = self.db.cursor() 
        self.offset = 0
        self.usr_ignore = [] 
        self.where_string = "" 
        self.interest_list = []
        self.gender = 0
        self.start_date = "" 
        self.experience_query = ExperienceQuery(host, user, pwd, db)

    # specify what users to ignore
    def ignore_members(self, ignore_list):

        self.usr_ignore = ignore_list

    # filters experiences in User object to get only experiences created on or after this date
    def filter_by_date(self, year, month, day):
        self.start_date = str(year) + "-" + str(month) + "-" + str(day)
    
    # filter by male or female, male = 1, female = 2 
    def filter_by_gender(self, gender):
        if gender < 1 or gender > 2:
            print 'enter 1 or 2. male = 1, female = 2'
            return
        self.gender = gender

    # set an interest vector to filter by
    def filter_by_interest(self, interest_list):
        if len(interest_list) != 45:
            print 'must be list of 45 {1, -1} values'
            return
        self.interest_list = interest_list

    # gets a chunk of users of specified size and filters
    def get_next_chunk(self, size):
        user_query = "select MB_Id, MB_InterestRaw from Members "
        where_string = ""
        #ignore list filter
        if len(self.usr_ignore) != 0:
            where_string += " and MB_Id != " + str(self.usr_ignore[0])
            for u in self.usr_ignore[1:]:
                where_string += " and MB_Id != " + str(u)

        # gender filter
        if self.gender != 0:
            where_string += " and MB_Sex = " + str(self.gender)
        # interest list filter
        if len(self.interest_list) != 0:
            where_string += " and MB_InterestRaw = '" + str(self.interest_list).replace(' ','') + "'"
        if where_string != "":
            where_string =  "where " + where_string[4:] # remove leading and         

        user_query += where_string + " limit " + str(size) + " offset " + str(self.offset)
        self.offset += size
        self.cur.execute(user_query)
        return [User(usr[0], self.experience_query, self.start_date, ast.literal_eval(usr[1])) for usr in self.cur.fetchall()]
    
    # resets the UserQuery        
    def reset(self):
        self.offset = 0
        self.usr_ignore = []
        self.interest_list = []
        self.gender = 0
        self.start_date = ""
        
# object repsention a row in the Experience table
class Experience:

    def __init__(self, values):
        self.EX_Id = values[0]
        self.EX_Created = values[1]
        self.EX_Modified = values[2]
        self.EX_LanguageId = values[3]
        self.EX_CH_ChannelNumber = values[4]
        self.EX_RG_RegionCode = values[5]
        self.EX_Description = values[6]
        self.EX_TimeOfDay = values[7]
        self.EX_SpecificTime = values[8]
        self.EX_ExpiryTime = values[9]
        self.EX_Place_PL_Id = values[10]
        self.EX_Category = values[11]
        self.EX_IM_Id = values[12]
        self.EX_Interests = values[13]
        self.EX_LikeCount = values[14]
        self.EX_ModerationScheme = values[15]
        self.EX_ModerationStatus = values[16]
        self.EX_MB_Id = values[17]
        self.EX_Style = values[18]
        self.EX_Vid_Id = values[19]

'''
Object to query the HeyLets db Experience table
Create a ExperienceQuery object. initialize the columns you want to filter by with
initialize, execute the query and return a list of Expereience objects with 
get_experiences or get_next_chunk
'''
class ExperienceQuery:
    
    def __init__(self, host, user, pwd, db):
        self.where_string = ""
        self.db = MySQLdb.connect(host=host,
                             user=user,
                             passwd=pwd,
                             db=db)

        self.cur = self.db.cursor() 
        self.offset = 0
        self.start_date = '0000-00-00'

    '''
    Call get_experiences to execute the query, by default it gets all experiences.
    for specific filters call initialize, to add member ids to ignore call 
    ignore_members
    '''
    def get_experiences(self):
        
        query_string = self.get_query_string()
        self.cur.execute(query_string)
        return [Experience(row) for row in self.cur.fetchall()]
    
    # join query for getting wishlisted Expereiences for a member
    def get_wishlisted_experiences(self, member_id):
        experience_member_query_string = "select Experience.* from ExperienceMember, Experience where ExperienceMember.EXM_MB_Id = " + str(member_id) + " and ExperienceMember.EXM_LikeCount > 0 and ExperienceMember.EXM_EX_id = Experience.EX_Id" 
        experience_member_query_string += " and Experience.EX_Created > '" + self.start_date + "'";
        self.cur.execute(experience_member_query_string)
        return [Experience(row) for row in self.cur.fetchall()]

    '''
    updates the query to ignore experiences with member ids in the list
    e.g to ignore member ids 4 and 5, 
    '''
    def ignore_members(self, member_list =[]):
        for mb in member_list:
            self.where_string += ' and EX_MB_Id != ' + str(mb)

    '''
    pass filters to the query object 
    e.g. if you want only experiences with EX_Place_PL_Id == 506 and EX_Category == 136
    call initialize(EX_Place_PL_Id=506, EX_Category=136) or  initialize({'EX_Place_PL_Id':506, 'EX_Category' :136})
    '''
    def initialize(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.where_string += ' and ' + str(key) + ' = ' + str(value)
    
    '''
    Gets the next chunk of results from the db for the given query. the size parameter is the
    upper limit for the number of experiences to return
     
    '''
    def get_next_chunk(self, size):

        query_string = self.get_query_string()
        self.cur.execute(query_string + " limit " + str(size) + " offset " + str(self.offset))
        self.offset = self.offset + size
        return [Experience(row) for row in self.cur.fetchall()]
 
    #add date filter to get experiences create on or after this date
    def filter_by_date(self, year, month, day):
        self.start_date = str(year) + "-" + str(month) + "-" + str(day)
     
    #helper method to get the query string based off specified filters
    def get_query_string(self):
        return "SELECT * FROM Experience where EX_Created > '" + self.start_date + "' " + self.where_string
    
    # resets the query
    def reset(self):
        self.where_string = ""
        self.offset = 0
        self.start_date = "0000-00-00"




class InterestLoader(object):
    
    def __init__(self, host, user, pwd, db):
        self.db = MySQLdb.connect(host=host,
                             user=user,
                             passwd=pwd,
                             db=db)

        self.cur = self.db.cursor() 

    # given a dictionary MB_id -> interestVector load into InterestVector table
    # max 1000 at a time
    def load_interests(self, interest_dict):
        insert_string = "INSERT INTO InterestVector VALUES"
        
        for MB_Id in interest_dict:
            insert_string += " (" + str(MB_Id)
            for entry in interest_dict[MB_Id]:
                insert_string += ", " + str(entry)
            insert_string += ")," 
        #qprint insert_string[:-1]
        try:
           # Execute the SQL command
           self.cur.execute(insert_string[:-1])
           # Commit your changes in the database
           self.db.commit()
        except:
           # Rollback in case there is any error
           self.db.rollback()



import MySQLdb

class CreateInterests(object):

    def __init__(self, host, user, pwd, db):
        self.db = MySQLdb.connect(host=host,
                             user=user,
                             passwd=pwd,
                             db=db)

        self.cur = self.db.cursor() 
    

    def createTable(self, vector_size):
        self.cur.execute("DROP TABLE IF EXISTS InterestVector") #check
        create_query = "CREATE TABLE InterestVector (IV_MB_Id Int(11) NOT NULL"
        for i in range(vector_size):
            create_query += ", I" + str(i) + " DECIMAL(10,4) NOT NULL"
        create_query += ", PRIMARY KEY (IV_MB_ID), FOREIGN KEY (IV_MB_ID) references Members(MB_Id)) ENGINE=INNODB"

        self.cur.execute(create_query)


