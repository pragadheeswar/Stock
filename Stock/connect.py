import sqlite3 as sql

conn = sql.connect('database.sqlite')
# conn.execute('CREATE TABLE Product (productID INTEGER PRIMARY KEY, productName TEXT,QTY INTEGER,productPrice INTEGER)')

# conn.execute("insert into product values(1,'Glass',20,5)")
# conn.execute("insert into product values(2,'Wood',10,9)")
# conn.execute("insert into product values(3,'Fuel',30,3)")
# conn.execute("insert into product values(4,'Steel',50,7)")

# conn.execute('''CREATE TABLE customer (customerID INTEGER PRIMARY KEY,customerName TEXT,customerPassword TEXT,
#                                         customerAddress text,customerMobile text,customerEmail text)''')

# conn.execute("insert into customer values(1,'User1','111','Street 1','9876543210','user1@gmail.com')")
# conn.execute("insert into customer values(2,'User2','222','Street 2','9846543210','user2@gmail.com')")
conn.execute("insert into customer (customerName,customerPassword,customerAddress,customerMobile,customerEmail) values(?,?,?,?,?)",('ds','sdf','dsaf','adsf','fd'))


# conn.execute("UPDATE Product SET QTY = QTY+? WHERE productID = ?",(20,2) )


conn.commit()
conn.close()