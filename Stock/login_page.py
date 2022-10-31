
import traceback
from requests import session
from flask import Blueprint , render_template,redirect,flash,request,url_for,session
import sqlite3 as sql

login_page=Blueprint("login_page",__name__,static_folder="static",template_folder="templates")

@login_page.route("/admin/",methods = ["GET","POST"])
def admin_login():
    if request.method=="POST":
        name=request.form["name"]
        password=request.form["password"]
        if(name=="admin" and password=="admin"):
            session["name"]=name

            return redirect(url_for("product"))
        else:
            flash("Username or Password Incorrect",'danger')
            return redirect(url_for("login_page.admin_login"))
    return render_template("a_login.html")

@login_page.route("/admin/logout",methods = ["GET","POST"])
def a_logout():
    session.clear()
    flash("Logout Successfully",'success')
    return redirect(url_for("login_page.admin_login"))


@login_page.route("/customer",methods = ["GET","POST"])
def c_login():
    if request.method=="POST":
        con = sql.connect("database.sqlite")
        cur = con.cursor()
        name=request.form["name"]
        password=request.form["password"]
        cur.execute("select * from customer where customerName=? and customerPassword=?",(name,password))
        data=cur.fetchone()
        con.close()
        if data:
            session["name"]=name
            # return redirect(url_for("supplier"))
            return redirect(url_for("customer"))
        else:
            flash("Username or Password Incorrect",'danger')
            return redirect(url_for("login_page.c_login"))
    return render_template("c_login.html")

@login_page.route("/customer/logout",methods = ["GET","POST"])
def c_logout():
    session.clear()
    flash("Logout Successfully",'success')
    return redirect(url_for("login_page.c_login"))


@login_page.route("/customer/register",methods = ["GET","POST"])
def c_register():
    if request.method=="POST":
        con = sql.connect("database.sqlite")
        cur = con.cursor()
        try:
            
            name=request.form["name"]
            password=request.form["password"]
            address=request.form["address"]
            mobile=request.form["mobile"]
            email=request.form["email"]
            print(name,password,address,mobile,email)

            cur.execute("insert into customer (customerName,customerPassword,customerAddress,customerMobile,customerEmail) values(?,?,?,?,?)",(name,password,address,mobile,email))

            flash("Registered",'success')
            con.commit()
        except Exception:
            # cur.roleback()
            traceback.print_exc()
            flash("Failed",'danger')
        finally:
            con.close()
            return redirect(url_for("login_page.c_login"))

    return render_template("c_register.html")


@login_page.route("/supplier",methods = ["GET","POST"])
def s_login():
    if request.method=="POST":
        name=request.form["name"]
        password=request.form["password"]
        if(name=="supplier" and password=="supplier"):
            session["name"]=name

            return redirect(url_for("supplier"))
        else:
            flash("Username or Password Incorrect",'danger')
            return redirect(url_for("login_page.s_login"))
    return render_template("s_login.html")


@login_page.route("/supplier/logout",methods = ["GET","POST"])
def s_logout():
    session.clear()
    flash("Logout Successfully",'success')
    return redirect(url_for("login_page.s_login"))