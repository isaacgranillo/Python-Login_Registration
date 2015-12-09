from system.core.model import *
from flask import Flask, flash
from flask.ext.bcrypt import Bcrypt
app = Flask(__name__)
flask_bcrypt = Bcrypt(app)
import re

class UserModel(Model):
    def __init__(self):
        super(UserModel, self).__init__()

    def create_user(self, info):

        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        
        errors = []
        
        if not info['first_name']:
            errors.append('First name cannot be blank')
        if len(info['first_name']) < 2:
            errors.append('First name must be at least 2 characters long')
        if not info['last_name']:
            errors.append('Last name cannot be blank')
        if len(info['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long')
        if not info['email']:
            errors.append('Email cannot be blank')
        if not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid')
        if not info['password']:
            errors.append('Password cannot be blank')
        if len(info['password']) < 8:
            errors.append('Password must be at least 8 chracters long')
        if info['password'] != info['password_confirm']:
            errors.append('Password and confirmation must match!')

        if errors:
            print errors
            return {"status": False, "errors": errors}
        else:
            passwordhash = flask_bcrypt.generate_password_hash(info['password'])
            insert_query = "INSERT INTO profiles (first_name, last_name, email, password ,created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', NOW(), NOW())".format(info['first_name'], info['last_name'], info['email'], passwordhash)
            self.db.query_db(insert_query)
            get_user_query = "SELECT * FROM profiles ORDER BY id DESC LIMIT 1"
            user = self.db.query_db(get_user_query)
            return {"status": True, "user": user[0]}

    def login_user(self, info):

        raw_password = info['password']
        signin_query = 'SELECT * FROM profiles WHERE EMAIL="{}"'.format(info['email'])
        user = self.db.query_db(signin_query)
        if user and flask_bcrypt.check_password_hash(user[0]['password'], raw_password):
            print 'LOGGED IN'
            user = self.db.query_db(signin_query)
            return {"status": True, "user": user[0]}
        else:
            errors = []
            errors.append("Invalid Login")
            return {"status": False, "errors": errors}
           






