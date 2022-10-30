from flask import Flask,render_template,redirect, url_for
from flask import request
from login_page import login_page
import sqlite3 as sql

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
   return  render_template('product.html',rows = rows) 


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
   return  render_template('supplier.html',rows = rows)



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

if __name__ == '__main__':
    app.run(port=5000,debug=True)