import cx_Oracle
from flask import *


# this file contains the general function of connecting to the server
# this function gets the db credentials from user input
def get_db_creds():
    username = request.form['username']
    password = request.form['password']
    hostname = request.form['hostname']
    port = request.form['port']
    sid = request.form['SID']
    creds = username + "/" + password + "@" + hostname + ":" + port + "/" + sid
    return creds


# this function connects to the db
def connect(db_credentials):
    try:
        con = cx_Oracle.connect(db_credentials)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    return con
