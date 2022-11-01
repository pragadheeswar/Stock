import traceback
from flask import Flask,render_template,redirect, url_for,session
from flask import request
from login_page import login_page
import sqlite3 as sql
import datetime

app = Flask(__name__)
app.register_blueprint(login_page,url_prefix="/login")
app.secret_key="dskjaf"

@app.route("/admin/product")
def product():
   con = sql.connect("database.sqlite")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from Product")
   
   rows = cur.fetchall();
   return  render_template('product.html',rows = rows,user=session["name"]) 


@app.route('/editProduct',methods = ['POST'])
def editProduct():
   if request.method == 'POST':
      con = sql.connect("database.sqlite")
      cur = con.cursor()


      try:
         productID = request.form['ProductID']
         productName = request.form['NEWProductName']
        #  productDescription=request.form['NEWProductDescription']
         ProductPrice=request.form['NEWProductPrice']
         cur.execute("UPDATE Product SET productName = ?,productPrice = ? WHERE productID = ?",(productName,ProductPrice,productID) )
         
         con.commit()
         msg = "Product Edited "
      except:
         con.rollback()
         msg = "error in operation"
      
      finally:
         con.close()
         return redirect(url_for('product')+"?msg="+msg)

@app.route('/admin/deleteProduct/<productID>')
def deleteProduct(productID):
      con = sql.connect("database.sqlite")
      cur = con.cursor()
      try:
            cur.execute("DELETE FROM Product WHERE productID = ?",(productID,))
            
            con.commit()
            msg = "Product Deleted"
      except:
            con.rollback()
            msg = "error in operation"
   
      finally:
            con.close()
            return redirect(url_for('product')+"?msg="+msg)


@app.route("/supplier")
def supplier():
   con = sql.connect("database.sqlite")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from Product")
   
   rows = cur.fetchall();
   name=session["name"]
   return  render_template('supplier.html',rows = rows,user=name)



@app.route('/addProduct',methods = ['POST'])
def addProduct():
   if request.method == 'POST':
      try:
         pn = request.form['pn']
         pq = request.form['pq']
         pp = request.form['pp']

        
         
         with sql.connect("database.sqlite") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Product (productName,QTY,productPrice) VALUES (?,?,?)",(pn,pq,pp) )
            
            con.commit()
            msg = "Record added"
      except:
         con.rollback()
         msg = "error in  operation"
      
      finally:
         con.close()
         return redirect(url_for('supplier')+"?msg="+msg)

@app.route('/editQTY',methods = ['POST'])
def editQTY():
   if request.method == 'POST':
      con = sql.connect("database.sqlite")
      cur = con.cursor()


      try:
         productID = request.form['ProductID']
         # productName = request.form['NEWProductName']
        #  productDescription=request.form['NEWProductDescription']
         ProductQTY=request.form['NEWProductQTY']
         print(productID,ProductQTY)
         cur.execute("UPDATE Product SET QTY = QTY+? WHERE productID = ?",(ProductQTY,productID) )
         
         con.commit()
         msg = "Product Edited "
      except:
         con.rollback()
         msg = "error in operation"
      
      finally:
         con.close()
         return redirect(url_for('supplier')+"?msg="+msg)


@app.route("/customer",methods=["GET","POST"])
def customer():
   con = sql.connect("database.sqlite")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from Product")
   
   rows = cur.fetchall();
   # print(session["user"])
   return  render_template('customer.html',rows = rows,user=session["name"])

@app.route("/buyProduct",methods=["GET","POST"])
def buyProduct():
   if request.method == 'POST':
      con = sql.connect("database.sqlite")
      cur = con.cursor()
      try:
         productID = request.form['ProductID']
         p = cur.execute("select productPrice from product where productID=?",(productID,))
         price = p.fetchone()
         # print(productPrice[0])
         productPrice =int(price[0])
        #  productDescription=request.form['NEWProductDescription']
         ProductName=request.form['NEWProductName']

         ProductQTY=request.form['NEWProductQty']
         print(productID,ProductQTY)
         print(session["name"])

         date = datetime.date.today().strftime("%d-%m-%Y")
         time = datetime.datetime.now().strftime("%I:%M%p")

         cost = int(ProductQTY)*productPrice

         cur.execute("UPDATE Product SET QTY = QTY-? WHERE productID = ?",(ProductQTY,productID) )

         cur.execute('''insert into purchase(customerName,productName,QTY,purchaseTime,purchaseDate,purchaseCost)
                        values(?,?,?,?,?,?)''',(session["name"],ProductName,ProductQTY,time,date,cost))
         con.commit()
         msg = "Product Edited "
      except Exception:
         con.rollback()
         msg = "error in operation"
         traceback.print_exc()
      
      finally:
         con.close()
         return redirect(url_for('customer')+"?msg="+msg)

@app.route("/admin/purchase",methods=["GET","POST"])
def purchase():
   con = sql.connect("database.sqlite")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from purchase")
   
   rows = cur.fetchall();
   # print(rows['purchaseDate'])
   # for row in rows:
   #    print(row)
   # print(type(rows))
   rows.reverse()
   return  render_template('purchase.html',rows = rows,user=session["name"])
   

if __name__ == '__main__':
    app.run(port=5005,debug=True)