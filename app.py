from flask import Flask, redirect, url_for, request,render_template,session, flash
import smtplib
import sqlite3 
import binascii
import hashlib
import snowflake.connector
from common import *
from flask import Flask
app = Flask(__name__)

#------------------------------Database details----------------------------
PASSWORD = 'Hinfo@123'
WAREHOUSE = 'COMPUTE_WH'
USER ='HINFO123'
ACCOUNT ='gmghmgv-iz89898'
DATABASE ='IOT1'
SCHEMA ='IOT'

# Connecting to the database file
conns = snowflake.connector.connect(
                user=USER,
                password=PASSWORD,
                account=ACCOUNT,
                warehouse=WAREHOUSE,
                database=DATABASE,
                schema=SCHEMA
                )
curs=conns.cursor()

#-------------dependency functions--------------------------------
@app.route('/clear')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('index'))

@app.route('/clear_purchaser')
def clearsession_purchaser():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('purchaser'))

#------------------------------------------------------------------


#------------------------------Vendor functions----------------------------
# @app.route('/vendor_login_portal')           
@app.route('/vendor_login_portal',methods=['GET','POST'])
def index(name=None):
    return render_template('HomePage.html',session=session,text=name)

@app.route('/vendor_dashboard',methods = ['POST', 'GET'])
def login():
    vendor_name = request.form['UserName']
    vendor_passwrd = request.form['Password']
    # password encryption
    vendor_password =encrypt(vendor_passwrd)

    #validate if all fields are entered
    if not vendor_name or not vendor_password:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('index', name=error))
    if login:
        query = ("select * from vendor1 where shopname = '%s' and password = '%s' " %(vendor_name,vendor_password))
        curs = conns.cursor().execute(query)
        #------debug_table_results You can print table results using print(results)-----------
        # results = debug_table(curs)
        return render_template('index.html', user1=vendor_name)
    
    else:
        error = "Username/Password is incorrect!"
        return redirect(url_for('index', name=error))
    
@app.route('/product_details',methods = ['POST', 'GET'])
def product_details():
        query = ("select * from product1")
        curs = conns.cursor().execute(query)
        results = debug_table(curs)
        product_details = sorted(results)
        return render_template('product_details.html',rows=product_details)

@app.route('/updateproducts', methods=['GET', 'POST'])
def updateproducts():
    id=request.form.get('ID')
    product_name=request.form.get('NAME')
    product_price=request.form.get('PRICE')
    prd_qty=request.form.get('QUANTITY')
    task = (id, product_name, product_price, prd_qty)
    sql = "update GradeTable set MidTerm1 = ?, MidTerm2 = ?, MidTerm3 = ?, FinalGrade = ? where SID = ? and FID = ? and CourseId = ?"
    curs = conns.cursor().execute(sql)
    a = curs.rowcount
    if a == 0:
        return 'no update happen'
    else:
    # commit and close connection
        return render_template('product_update.html')


@app.route('/purchaser_details',methods = ['POST', 'GET'])
def purchaser_details():
        query = ("select * from customer")
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()
        return render_template('purchaser_details.html',rows=results,)

@app.route("/create_purchaser",methods=['GET','POST'])
def create_purchaser():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        phone=request.form['phone']
        curs=conns.cursor()
        sql="INSERT INTO customer(User_Name,Email_id,User_Address,Telephone) values (%s,%s,%s,%s)"
        value = (name,email,address,phone)
        curs = conns.cursor().execute(sql,value)
        conns.commit()
        flash('customer added successfully','success')
        return redirect(url_for("purchaser_details"))
    return render_template("create_purchaser.html")

@app.route('/edit_purchaser/<string:id>',methods = ['POST','GET'])  
def edit_purchaser(id):
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        phone=request.form['phone']
        curs=conns.cursor()
        task = "update customer set User_Name = %s, Email_id = %s,User_Address = %s,Telephone = %s WHERE Rfid_Id = %s"
        value = (name,email,address,phone,id)
        curs = conns.cursor().execute(task,value)
        flash('customer updated successfully','success')
        return redirect (url_for('purchaser_details'))
    
    if request.method=='GET':
        curs=conns.cursor()
        sql="select * from customer where Rfid_Id= %s"
        curs = conns.cursor().execute(sql,[id])
        results = curs.fetchone()
        print("---------------test-----------")
        print(results)
        return render_template("edit_purchaser.html", results = results)
    
@app.route('/delete_purchaser/<string:id>',methods = ['POST', 'GET'])  
def delete_purchaser(id):
    curs=conns.cursor()
    sql="delete from customer where Rfid_Id=%s"
    curs = conns.cursor().execute(sql,[id])
    flash('customer deleted successfully','success')
    return redirect(url_for("purchaser_details"))

@app.route('/activate_purchaser/<string:id>',methods = ['POST','GET'])  
def activate_purchaser(id):
    curs=conns.cursor()
    sql="update customer set Status = 'True' WHERE Rfid_Id = %s"
    curs = conns.cursor().execute(sql,[id])
    return redirect(url_for("purchaser_details"))

@app.route('/deactivate_purchaser/<string:id>',methods = ['POST','GET'])  
def deactivate_purchaser(id):
    curs=conns.cursor()
    sql="update customer set Status = 'False' WHERE Rfid_Id = %s"
    curs = conns.cursor().execute(sql,[id])
    return redirect(url_for("purchaser_details"))


####----------------------------Purchaser functions-------------------------------------------------

@app.route('/purchaser',methods=['GET','POST'])
def purchaser(name=None):
    return render_template('purchaser_login.html',session=session,text=name)


@app.route('/purchaser_dashboard',methods = ['POST', 'GET'])
def purchaser_dashboard():
    user_id = request.form['UserName']
    user_id=encrypt(user_id)
    print(user_id)
    pwd1 = request.form['Password']
    pwd=encrypt(pwd1)
    print (pwd)
    #validate if all fields are entered
    if not user_id or not pwd:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('purchaser', name=error))

    query = ("select * from purchaser1 where id = '%s' and password = '%s' " %(user_id,pwd))

    curs = conns.cursor().execute(query)
    query_id = curs.sfqid
    curs.get_results_from_sfqid(query_id)
    results = curs.fetchall()

    if results:
        query = ("select * from purchaser_dashboard")
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()
        mytuple = sorted(results)
        print(results)
        return render_template('purchaser_dashboard.html',rows=mytuple)
    else:
        error = "Username/Password is incorrect!"
        return redirect(url_for('purchaser', name=error))


if __name__ == '__main__':
    app.secret._key='hinfo@123'
    app.run(use_reloader=True)