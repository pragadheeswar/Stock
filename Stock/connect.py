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
# conn.execute("insert into customer (customerName,customerPassword,customerAddress,customerMobile,customerEmail) values(?,?,?,?,?)",('ds','sdf','dsaf','adsf','fd'))


# conn.execute("UPDATE Product SET QTY = QTY+? WHERE productID = ?",(20,2) )

# conn.execute('''create table purchase(purchaseID integer primary key ,customerName test,
#                 productName text,QTY integer,purchaseTime text,purchaseDate text,purchaseCost integer)''')
# conn.execute("insert into purchase values(1,'User1','Glass',10,'07:36PM','01-11-2022',20)")

# conn.execute('''CREATE TABLE request (requestID integer primary key,requestName text,
#                                         requestQTY interger) ''')
conn.execute("alter table request add column requestPrice integer")

# conn.execute("insert into request values (1,'Glass',10)")
conn.execute("delete from request")
conn.commit()
conn.close()