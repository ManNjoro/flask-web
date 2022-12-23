import mysql.connector
from flask import request
from flask import Flask
from flask_mysqldb import MySQL
from flask_login import UserMixin

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="",
#     database="mosh"
# )
# mycursor = mydb.cursor()
class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json
    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)