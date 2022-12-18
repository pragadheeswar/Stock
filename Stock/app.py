import traceback
from flask import Flask,render_template,redirect, url_for,session,flash
from flask import request
from login_page import login_page
import sqlite3 as sql
import datetime

app = Flask(__name__)
app.register_blueprint(login_page,url_prefix="/login")
app.secret_key="dskjaf"


@app.route("/")
def home():
   
   return render_template("home.html")

@app.route("/admin/product")
def product():
   con = sql.connect("database.sqlite")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from Product")
   
   rows = cur.fetchall();
   con.close()
   return  render_template('product.html',rows = rows,user=session["name"]) 

@app.route("/admin")
def dashboard():
   con = sql.connect("database.sqlite")
   # con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select productName,QTY from Product order by QTY desc")
   rows = cur.fetchmany(8)
   lables = [row[0] for row in rows]
   data = [row[1] for row in rows]
   # print(lables,data)
   # print("helo")
   con.close()
   return render_template("dashboard.html",lables=lables,data=data)

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
         flash("Product Edited","success")
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
            flash("Product Deleted","danger")
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
         productName = request.form['NEWProductName']
        #  productDescription=request.form['NEWProductDescription']
         ProductQTY=request.form['NEWProductQTY']
         print(productID,ProductQTY)
         cur.execute("UPDATE Product SET QTY = QTY+? WHERE productID = ?",(ProductQTY,productID) )
         cur.execute("UPDATE Product SET productName = ? WHERE productID = ?",(productName,productID) )

         
         con.commit()
         msg = "Product Edited "
      except Exception:
         con.rollback()
         traceback.print_exc()
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

         old=cur.execute("Select QTY from product where productID = ?",(productID,))
         old=old.fetchone()
         # print(old[0])
         oldQTY = int(old[0])

         if(int(ProductQTY) <= oldQTY):
            date = datetime.date.today().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%I:%M%p")

            cost = int(ProductQTY)*productPrice

            cur.execute("UPDATE Product SET QTY = QTY-? WHERE productID = ?",(ProductQTY,productID) )

            cur.execute('''insert into purchase(customerName,productName,QTY,purchaseTime,purchaseDate,purchaseCost)
                           values(?,?,?,?,?,?)''',(session["name"],ProductName,ProductQTY,time,date,cost))
            con.commit()
            msg = "Product Edited "
            flash("Product Purchased","success")
         else:
            flash("This much of stock is not available","error")
            msg= "no stock"
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
   
@app.route('/requestProduct',methods = ['POST'])
def requestProduct():
   if request.method == 'POST':
      try:
         pn = request.form['pn']
         pq = request.form['pq']
         # pp = request.form['pp']

        
         
         with sql.connect("database.sqlite") as con:
            cur = con.cursor()
            id = cur.execute("select productID from product where ProductName = ?",(pn,))
            id = id.fetchone()
            if id is None:
               cur.execute("INSERT INTO request (requestName,requestQTY) VALUES (?,?)",(pn,pq) )
            else:
               cur.execute("INSERT INTO request (requestName,requestQTY,requestPrice) VALUES (?,?,?)",(pn,pq,id[0]) )
               
            con.commit()
            flash("Request sent","success")
            msg = "Record added"
      except:
         con.rollback()
         msg = "error in  operation"
      
      finally:
         con.close()
         return redirect(url_for('product')+"?msg="+msg)

@app.route("/request",methods=["GET","POST"])
def supplierRequest():
   con = sql.connect("database.sqlite")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from request")
   
   rows = cur.fetchall();
   # print(f)
   # print(session["user"])
   # if f !=None:
   # flash(s,"success")
   if request.method == 'POST':
      flash("hello","success")

   return  render_template('supplier_req.html',rows = rows,user=session["name"])

@app.route("/giveRequest",methods=["GET","POST"])
def giveRequest():
   if request.method == 'POST':
      con = sql.connect("database.sqlite")
      cur = con.cursor()


      try:
         productName = request.form['NEWProductName']
         productQTY=request.form['NEWProductQTY']
         productPrice = request.form['NEWProductPrice']

         # print(productName,ProductQTY,productPrice)
         id = cur.execute("select productID from product where ProductName = ?",(productName,))
         id = id.fetchone()
         if id is None:
            cur.execute("INSERT INTO Product (productName,QTY,productPrice) VALUES (?,?,?)",(productName,productQTY,productPrice))
         else:
            # cur.execute()
            cur.execute("UPDATE Product SET QTY = QTY+? WHERE productID = ?",(productQTY,id[0]) )

         # cur.execute("UPDATE Product SET productName = ? WHERE productID = ?",(ProductName,productID) )

         
         con.commit()
         msg = "Product Edited "
      except:
         con.rollback()
         msg = "error in operation"
      
      finally:
         con.close()
         return redirect(url_for('supplierRequest')+"?msg="+msg)
@app.route("/supplyNewProduct",methods=["GET","POST"])
def supplyNewProduct():
   if request.method == 'POST':
      con = sql.connect("database.sqlite")
      try:
         cur = con.cursor()

         requestID=request.form["ProductID"]
         productName=request.form["NEWProductName"]
         productQTY = request.form["NEWProductQTY"]
         productPrice = request.form["NEWProductPrice"]
         # print(requestID,productName,productQTY,productPrice)
         cur.execute("INSERT INTO Product (productName,QTY,productPrice) VALUES (?,?,?)",(productName,productQTY,productPrice))
         cur.execute("DELETE FROM request WHERE requestID = ?",(requestID,))
         # print(requestID)
         con.commit()
         msg = "Added"
         # return redirect(url_for('supplierRequest'))
      except:
         con.rollback()
         msg = "error in operation"
      finally:
         con.close()
         return redirect(url_for('supplierRequest')+"?msg="+msg)

@app.route("/supplyProduct",methods=["GET","POST"])
def supplyProduct():
   if request.method == 'POST':
      con = sql.connect("database.sqlite")
      cur = con.cursor()
      try:
         requestID=request.form["ADDProductID"]
         productName=request.form["ADDProductName"]
         productQTY = request.form["ADDProductQTY"]
         cur.execute("UPDATE Product SET QTY = QTY+? WHERE productName = ?",(productQTY,productName) )
         cur.execute("DELETE FROM request WHERE requestID = ?",(requestID,))
         con.commit()
         msg = "Added"
      except:
         con.rollback()
         msg = "error in operation"
         # print(requestID,productName,productQTY)
         flash("Product Added","success")
      finally:
         con.close()
         return redirect(url_for('supplierRequest')+"?msg="+msg)     


         # productPrice = request.form["NEWProductPrice"]

if __name__ == '__main__':
    app.run(port=5000,debug=True)