import sqlite3
import hashlib
import random
import string

##
##conn = sqlite3.connect('Smart_Gates_DB.db')
##
##c = conn.cursor()
##data = []
##
##c.execute('DROP TABLE events')
##c.execute('DROP TABLE reminders')
##
###c.execute("SELECT * FROM users")
##temp = c.fetchall()
##print(temp)
##conn.commit()
##conn.close()

#c.execute("""create table employees (
#             email       text,
#             first_name  text,
#             last_name   text,
#             pass        text
#             )""")

#c.execute("INSERT INTO employees VALUES ('John_Doe@gmail.com', 'John', 'Doe', '12345')")
#c.execute("INSERT INTO employees VALUES ('Jane_Doe@gmail.com', 'Jane', 'Doe', '12345')")
#c.execute("INSERT INTO employees VALUES ('Jack_Doe@gmail.com', 'Jack', 'Doe', '12345')")

#uname = "Jack"
#pswd = "12345"

#find_user = ("SELECT * FROM employees WHERE first_name = ? AND pass = ?")
#c.execute(find_user, [(uname), (pswd)])
#results = c.fetchall()

#print(len(results))


class Smart_Gates_Database():
    
    def __init__(self):
        pass

    # returns > 0 if table exists
    def table_exists(self, table_name):
        
        # connect to database, establish cursor
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()

        # check if the table exists
        table_exists = ("SELECT name FROM sqlite_master WHERE type='table' AND name= ? ")
        c.execute(table_exists, [(table_name)])
        results = c.fetchall()

        conn.commit()
        conn.close()

        return len(results)

    # creates the users table if it does not already exist
    def create_user_table(self):

        # connect to database, establish cursor
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()

        if self.table_exists("users") ==  0:
            
            # create the user table
            c.execute("""create table users (
                 id       integer,
                 tag      text
                 )""")

        # commit and close connection
        conn.commit()
        conn.close()

    def create_events_table(self):
        
        # connect to database, establish cursor
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()

        if self.table_exists("events") ==  0:
            
            # create the events table
            c.execute("""create table events (
                 eventID        integer,
                 title          text,
                 description    text,
                 start_time     text,
                 end_time       text,
                 creatorID      integer,
                 attendeeID     integer
                 )""")

        # commit and close connection
        conn.commit()
        conn.close()

    def create_attendee_table(self):
        
        # connect to database, establish cursor
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()

        if self.table_exists("attendees") ==  0:
            
            # create the attendees table
            c.execute("""create table attendees (
                 id             integer,
                 email          text,
                 attendeeID     interger
                 )""")

        # commit and close connection
        conn.commit()
        conn.close()


    def create_reminders_table(self):
        
        # connect to database, establish cursor
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()

        if self.table_exists("reminders") ==  0:
            
            # create the events table
            c.execute("""create table reminders (
                 remID          integer,
                 title          text,
                 description    text,
                 start_time     text,
                 creatorID      integer
                 )""")

        # commit and close connection
        conn.commit()
        conn.close()

    def find_user_by_tag(self, tag):
        
        # make sure that the RFID Tag is unique
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()

        # check against the database
        find_user = ("SELECT * FROM users WHERE tag = ?")
        c.execute(find_user, [(tag)])

        # get results
        results = c.fetchall()
        conn.commit()
        conn.close()
        return results

    # generates a unqiue tag pair for the user
    def generate_tag(self):
        
        generated = 0
        while generated == 0:

            ## length of unhashed RFID Tag
            N = 64
        
            # generate unhashed RFID Tag
            not_hashed_tag = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

            # make sure that the RFID Tag is unique
            not_unique = self.find_user_by_tag(not_hashed_tag)

            # if it is return the newly genrated tag pair
            if len(not_unique) == 0:
                generated = 1

        return not_hashed_tag


    def add_new_user(self, id, RFIDtag):
        
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()

        enter_user = ("INSERT INTO users VALUES ( ?, ?)")
        c.execute(enter_user, [(id), (RFIDtag)])

        # commit and close connection
        conn.commit()
        conn.close()

    def get_id(self, tag):
        
        # connect to database, establish cursor
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()

        # match tag to id
        find_id = ("SELECT id FROM users WHERE tag = ?")
        c.execute(find_id, [(tag)])
        results = c.fetchone()

        # commit and close connection
        conn.commit()
        conn.close()

        # return the id number 
        return results[0]
    
    def create_event(self, data, num):
        
        # connect to database, establish cursor
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()

        enter_event = ("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?)")
        
        for x in range(num):
            c.execute(enter_event, [(data[7*x]), (data[7*x+1]), (data[7*x+2]), (data[7*x+3]), (data[7*x+4]), (data[7*x+5]), (data[7*x+6])])

        # commit and close connection
        conn.commit()
        conn.close()
    
    def create_reminder(self, data, num):
        
        # connect to database, establish cursor
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()

        enter_event = ("INSERT INTO reminders VALUES (?, ?, ?, ?, ?)")
        
        for x in range(num):
            c.execute(enter_event, [(data[5*x]), (data[5*x+1]), (data[5*x+2]), (data[5*x+3]), (data[5*x+4])])

        # commit and close connection
        conn.commit()
        conn.close()
    
    def get_reminders(self):
        
        # connect to database, establish cursor
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM reminders")
        reminders = c.fetchall()
        
        # commit and close connection
        conn.commit()
        conn.close()
        
        return reminders

    def get_events(self):
        
        # connect to database, establish cursor
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM events")
        events = c.fetchall()
        
        # commit and close connection
        conn.commit()
        conn.close()
        
        return events
    
    def login_RFID(self, tag):
        
        # connect to database, establish cursor
        conn = sqlite3.connect('Smart_Gates_DB.db')
        c = conn.cursor()
        
        login = ("SELECT * FROM users WHERE tag == ?")
        c.execute(login, [(tag)])
        count = c.fetchall()
        
        # commit and close connection
        conn.commit()
        conn.close()
        
        return len(count)

## testing
#create user table
#test = Smart_Gates_Database()
#test.create_user_table()
#print(test.get_id('X1B9OJWNRMGFZOYUN5K7AHUM1KO1XOEC1UOJHX8PNTRPV6IA909TLMV7CTC5ONNJ'))
#a = test.generate_tag()


        