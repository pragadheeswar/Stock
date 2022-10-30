import sqlite3 as sql

conn = sql.connect('database.sqlite')
# conn.execute('CREATE TABLE Product (productID INTEGER PRIMARY KEY, productName TEXT,QTY INTEGER,productPrice INTEGER)')

# conn.execute("insert into product values(1,'Glass',20,5)")
# conn.execute("insert into product values(2,'Wood',10,9)")
# conn.execute("insert into product values(3,'Fuel',30,3)")
# conn.execute("insert into product values(4,'Steel',50,7)")


conn.execute("UPDATE Product SET QTY = QTY+? WHERE productID = ?",(20,2) )


conn.commit()
conn.close()