import sqlite3
import hashlib

conn = sqlite3.connect('Smart_Gates_DB.db')

c = conn.cursor()

##c.execute("""CREATE TABLE employees (
##             email       text,
##             first_name  text,
##             last_name   text,
##             pass        text
##             )""")
##
##c.execute("INSERT INTO employees VALUES ('John_Doe@gmail.com', 'John', 'Doe', '12345')")
##c.execute("INSERT INTO employees VALUES ('Jane_Doe@gmail.com', 'Jane', 'Doe', '12345')")
##c.execute("INSERT INTO employees VALUES ('Jack_Doe@gmail.com', 'Jack', 'Doe', '12345')")

#c.execute("SELECT first_name FROM employees")

#conn.commit()

uname = "12345"
pswd = "12345"
pswd = hashlib.sha256(uname.encode()).hexdigest()

find_user = ("SELECT * FROM employees WHERE first_name = ? AND pass = ?")
c.execute(find_user, [(uname), (pswd)])
results = c.fetchall()

print(pswd)

conn.commit()

conn.close()