import sqlite3

conn = sqlite3.connect('signin/Smart_Gates_DB.db')

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

uname = "Jack"
pswd = "12345"

find_user = ("SELECT * FROM employees WHERE first_name = ? AND pass = ?")
c.execute(find_user, [(uname), (pswd)])
results = c.fetchall()

print(results)

conn.commit()

conn.close()