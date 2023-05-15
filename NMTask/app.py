from flask import Flask, app, flash, redirect, render_template, request, redirect, session, url_for
import ibm_db
import ibm_db_dbi as dbi
from pyodbc import connect
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
# Database credentials
database = "bludb"
hostname = "3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
port = "31498"
username = "qwh90818"
password = "d8O436rEebMYO5NH"
ssl_cert = "DigiCertGlobalRootCA.crt"

# Establish a connection to the IBM Db2 database
connect = f"DATABASE={database};HOSTNAME={hostname};PORT={port};PROTOCOL=TCPIP;UID={username};PWD={password};SECURITY=SSL;SSLServerCertificate={ssl_cert};"
conn = ibm_db.connect(connect, '', '')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginuser', methods=['POST'])
def loginuser():
    x = [x for x in request.form.values()]
    EMAIL = x[0]
    PASSWORD = x[1]
    sql = "SELECT * FROM auth WHERE EMAIL = ? AND PASSWORD = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, EMAIL)
    ibm_db.bind_param(stmt, 2, PASSWORD)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
        return render_template('profile.html', user=account)
    else:
        error = "Invalid email or password !"
        return render_template('login.html', error=error)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register1', methods=['POST'])
def register1():
    x = [x for x in request.form.values()]
    NAME = x[0]
    EMAIL = x[1]
    PASSWORD = x[2]

    # Check if any input field is empty
    if not NAME or not EMAIL or not PASSWORD:
        error = "Please fill in all the required fields!"
        return render_template('register.html', error=error)

    # Check if the user already exists
    sql = "SELECT * FROM auth WHERE EMAIL = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, EMAIL)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
        return render_template('login.html', error="You are already a member. Please login using your details!")
    else:
        # Insert the new user into the database
        insert_sql = "INSERT INTO auth (NAME, EMAIL, PASSWORD) VALUES (?, ?, ?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, NAME)
        ibm_db.bind_param(prep_stmt, 2, EMAIL)
        ibm_db.bind_param(prep_stmt, 3, PASSWORD)
        ibm_db.execute(prep_stmt)
        return render_template('login.html', message="Registration successful. Please login using your details!")

@app.route('/logout', methods=['POST'])
def logout():
    return render_template('login.html', message="Logged out !")

if __name__ == '__main__':
    app.run()
