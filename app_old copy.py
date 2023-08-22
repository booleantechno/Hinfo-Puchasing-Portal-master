from flask import Flask, redirect, url_for, request,render_template,session, flash
import smtplib
import sqlite3 
import binascii
import hashlib
import snowflake.connector

from flask import Flask
app = Flask(__name__)
PASSWORD = 'Hinfo@123'
WAREHOUSE = 'COMPUTE_WH'
USER ='HINFO123'
ACCOUNT ='gmghmgv-iz89898'
DATABASE ='IOT1'
SCHEMA ='IOT'

conns = snowflake.connector.connect(
                user=USER,
                password=PASSWORD,
                account=ACCOUNT,
                warehouse=WAREHOUSE,
                database=DATABASE,
                schema=SCHEMA
                )
curs=conns.cursor()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/purchaser',methods=['GET','POST'])
def purchaser(name=None):
    return render_template('purchaser_login.html',session=session,text=name)

@app.route('/success/<name>',methods=['GET','POST'])
def success(name):
    return name

@app.route('/successfully',methods=['GET','POST'])
def successfully():
    return success    

@app.route('/forgotpassword',methods=['GET','POST'])
@app.route('/forgotpassword/<name>')
def forgotpassword(name=None):
   return render_template('Forgot.html',text=name)

@app.route('/rfid_login',methods=['GET','POST'])
    
def flask():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM user').fetchall()
    conn.close()
    return render_template('index.html')

def rfid_login():
    if request.method == 'GET':
        rfid = int(request.json['num1'])
        query =("select * from token where ID = %s"% (rfid))
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()
        if results:
            available = 1
            return f'{available}'
        else:
            available = 0
            return f'{available}'

@app.route("/reset_password", methods=['GET'])
def reset_password():
    email = request.args.get('email')
    print(email)
    return render_template('reset_password.html', email=email)





# @app.route("/reset_password", methods=['POST', 'GET'])
# def reset_password():
#     if request.method == 'GET':
#         email = request.args.get('email_id')
#         curs=conns.cursor()
#         sql=("select * from vendor1 where email_id = '%s' "%(email))
#         print("------------testingstart-----------")
#         print(sql)
#         print("------------testingend-----------")
#         curs = conns.cursor().execute(sql)
#         results = curs.fetchone()
#         print("------------testingstart-----------")
#         print(results)
#         print("------------testingend-----------")
#         return render_template('reset_password.html', email=email)

@app.route('/resetpass',methods = ['POST', 'GET'])
def resetpass():
    if request.method == 'POST':
        mail = request.form['email']
        print(mail)
        passw = request.form['new_password']
        # password encryption
        pwd = hashlib.md5(passw.encode())
        passw = pwd.hexdigest()
        print("-----------test1start-------------")
        print(request.form)
        print("-----------test1end-------------")
        
        if mail is None:
            error = "Invalid/Unknown mail."
            return redirect(url_for('reset_password', name=error))

        query = ("select * from vendor1 where email_id = '%s' " %(mail))
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchone()
        print("********************check results**********************")
        print(results)  

        
        if results:
            print(mail)
            print(passw)
            query = ("update vendor1 set password = '%s' WHERE email_id = '%s' "%(passw,mail))
            curs = conns.cursor().execute(query)
            query_id = curs.sfqid
            curs.get_results_from_sfqid(query_id)
            results = curs.fetchall()
            print(results)
            return render_template('reset_password.html',results=results)
        
        else:
            error = "mail is incorrect!"
            return redirect(url_for('reset_password', name=error))
        
    # print("------------testingstart-----------")
    # print(request.method)
    # print("------------testingend-----------")
    # curs=conns.cursor()
    # sql=("select * from vendor1 where shopname = '%s' "%(shopname))
    # print("------------testingstart-----------")
    # print(sql)
    # print("------------testingend-----------")
    # curs = conns.cursor().execute(sql)
    # results = curs.fetchone()
    # user=results['shopname']
    # user1=session['shopname']
    # if user == user1:
    #     return render_template('reset_password.html', results=results)
    # else:
    #     return redirect('/')
    # if request.method=='GET':
    #     print("------------testingstart-----------")
    #     print(request.method)
    #     print("------------testingend-----------")
    #     mail = request.form['email']
    #     print(mail)
    #     query = ("select email_id from vendor1 where shopname = '%s'"%(mail))
    #     curs = conns.cursor().execute(query)
    #     query_id = curs.sfqid
    #     curs.get_results_from_sfqid(query_id)
    #     results = curs.fetchone()
    #     print(results)
    #     return render_template('reset_password.html', results=results)    
    

@app.route('/purchasing_list',methods = ['POST', 'GET'])
def purchasing_list():
    curs=conns.cursor()
    sql="select * from purchasing_list"
    curs = conns.cursor().execute(sql)
    results = curs.fetchall()
    print(results)
    mytuple = sorted(results)
    return render_template("purchasing_list.html", rows = mytuple)


@app.route('/purchaser_view/<string:id>',methods = ['POST', 'GET'])
def purchaser_view(id):
    curs=conns.cursor()
    sql="select * from purchasing_list WHERE ID= %s"
    print(sql)
    curs = conns.cursor().execute(sql,[id])
    results = curs.fetchall()
    print(results)
    return render_template("purchaser_view.html", rows=results)

@app.route('/purchasersignup',methods=['GET','POST'])
def purchasersignup():
   return render_template('Purchaser_signup.html')        
    

    
# @app.route('/forgothandling',methods = ['POST', 'GET'])
# def forgothandling():
#     email = request.form['Email']
#     action = request.form.get('action', '')

#     if not email or not action:``
#         error = "Any of the fields cannot be left blank"
#         return redirect(url_for('forgotpassword', name=error))

#     if action == '':
#         c.execute("select decryption(Password) from where email = ?", (email,))
#         f = c.fetchone()
#         if not f:
#             error = "Email entered is incorrect!"
#             return redirect(url_for('forgotpassword', name=error))
#         else:
#         message = "An Email containing password has been sent to your registered email ID"
#         return redirect(url_for('forgotpassword', name=message))
#     elif action == 'Faculty':
#         c.execute("select decryption(Password) from FacultyLoginTable where Email = ?", (email,))
#         f = c.fetchall()
#         if not f:
#             error = "Email entered is incorrect!"
#             return redirect(url_for('forgotpassword', name=error))
#         else:
#             to = email
#             gmail_user = 'studentacademyportal@gmail.com'
#             gmail_pwd = 'hellostudent'
#             smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
#             smtpserver.ehlo()
#             smtpserver.starttls()
#             smtpserver.ehlo()  # extra characters to permit edit
#             smtpserver.login(gmail_user, gmail_pwd)
#             header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Confidential Message \n'
#             print(header)
#             msg = header + '\n This message contains your password to Student Academic Portal \n\n' + str(f)
#             smtpserver.sendmail(gmail_user, to, msg)
#             print("done!")
#             smtpserver.quit()
#             message = "An Email containing password has been sent to your registered email ID"
#             return redirect(url_for('forgotpassword', name=message))

@app.route('/clear_admin')
def clearsession_admin():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('admin'))



@app.route('/signup', methods=['GET', 'POST'])

def signup():

    # Connecting to the database file
    curs=conns.cursor()
    name = request.form['Name']
    action = request.form.get('action', '')
    user1 = request.form['UserName']
    user=encrypt(user1)
    email = request.form['email']

    # validate if all fields are entered
    # if not action or not user or not pwd or not email or not name:
    #     error = "Any of the fields cannot be left blank"
    #     return redirect(url_for('success', name=error))

    # validate if all fields are entered
    if not action:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('success', name=error))

    if action == 'Add':
        if not action or not user or not email or not name:
            error = "Any of the fields cannot be left blank"
            return redirect(url_for('success', name=error))

        query =("select * from purchaser1 where ID = %s"% (user1))
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()
 
        if results:
            msg = "User already exists"
        else:
            curs.execute("INSERT INTO purchaser1(ID, USERNAME,EMAIL_ID) ""VALUES(%s, %s, %s)", (user,name,email))
            msg = "User has been registered successfully"

        return redirect(url_for('success', name=msg))
    elif action == 'Remove':
        if not user:
            error = "Enter user and name fields cannot be left blank"
            return redirect(url_for('success', name=error))
        query =("select * from purchaser1 where ID = %s"% (user1))
        curs = conns.cursor().execute(query)
        query_id = curs.sfqid
        curs.get_results_from_sfqid(query_id)
        results = curs.fetchall()

        if results:
            curs.execute("DELETE FROM purchaser1 where ID = %s"%(user))
            msg = "User has been removed successfully"
        else:
            msg = "User doesn't exists"
        return redirect(url_for('success', name=msg))

@app.route('/admin',methods=['GET','POST'])
def admin(name=None):
    return render_template('admin_login.html',session=session,text=name)

@app.route('/admin_dashboard',methods = ['POST', 'GET'])
def admin_dashboard():
    user_name = request.form['UserName']
    user_name=encrypt(user_name)
    print(user_name)
    pwd1 = request.form['Password']
    pwd=encrypt(pwd1)
    print (pwd)
    #validate if all fields are entered
    if not user_name or not pwd:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('admin', name=error))

    query = ("select * from admin where user_name = '%s' and password = '%s' " %(user_name,pwd))
    curs = conns.cursor().execute(query)
    query_id = curs.sfqid
    curs.get_results_from_sfqid(query_id)
    results = curs.fetchall()

    if results:
        return render_template('admin_dashboard.html')
    else:
        error = "Username/Password is incorrect!"
        return redirect(url_for('admin', name=error))


@app.route('/shop_list',methods = ['POST', 'GET'])
def shop_list():
    query = ("select * from shop_list")
    curs = conns.cursor().execute(query)
    query_id = curs.sfqid
    curs.get_results_from_sfqid(query_id)
    results = curs.fetchall()
    mytuple = sorted(results)
    print(results)
    return render_template('shop_list.html',rows=mytuple)



@app.route('/shop_view/<string:id>',methods = ['POST', 'GET'])
def shop_view(id):
    curs=conns.cursor()
    sql="select * from shop_list WHERE ID= %s"
    print(sql)
    curs = conns.cursor().execute(sql,[id])
    results = curs.fetchall()
    print(results)
    return render_template("shop_view.html", rows=results)

@app.route('/activate_shop/<string:id>',methods = ['POST','GET'])  
def activate_shop(id):
    curs=conns.cursor()
    sql="update shop_list set Status = 'True' WHERE ID = %s"
    curs = conns.cursor().execute(sql,[id])
    return redirect(url_for("shop_view"))

@app.route('/deactivate_shop/<string:id>',methods = ['POST','GET'])  
def deactivate_shop(id):
    curs=conns.cursor()
    sql="update shop_list set Status = 'False' WHERE ID = %s"
    curs = conns.cursor().execute(sql,[id])
    return redirect(url_for("shop_view"))


@app.route('/delete_shop/<string:id>',methods = ['POST', 'GET'])  
def delete_shop(id):
    curs=conns.cursor()
    sql="delete from shop_list where ID=%s"
    curs = conns.cursor().execute(sql,[id])
    flash('customer deleted successfully','success')
    return redirect(url_for("shop_list"))    


@app.route('/adminsignup',methods=['GET','POST'])
def adminsignup():
   return render_template('admin_signup.html')

if __name__ == '__main__':
    app.secret._key='hinfo@123'
    app.run(use_reloader=True)