from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.emaii = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) \
                VALUES (%(fname)s, %(lname)s, %(email)s, %(pword)s, NOW(), NOW());"
        result = connectToMySQL('dojo_wall_schema').query_db(query, data)
        return result
    
    @classmethod
    def select_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        result = connectToMySQL('dojo_wall_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def select_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL('dojo_wall_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('dojo_wall_schema').query_db(query, data)
        if len(data['fname']) == 0:
            flash("First Name cannot be blank!", "create")
            is_valid = False
        elif len(data['fname']) <= 1:
            flash("First Name has to be longer than one character!", "create")
            is_valid = False
        if len(data['lname']) == 0:
            flash("Last Name cannot be blank!", "create")
            is_valid = False
        elif len(data['lname']) <= 1:
            flash("Last Name has to be longer than one character!", "create")
            is_valid = False
        if len(data['email']) == 0:
            flash("Email cannot be blank!", "create")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email Address!", "create")
            is_valid = False
        elif len(result) >= 1:
            flash("Email is already in use!", "create")
            is_valid = False
        if len(data['pword']) == 0:
            flash("Password cannot be blank!", "create")
            is_valid = False
        elif len(data['pword']) <= 7:
            flash("Password must be longer than 7 characters!", "create")
            is_valid = False
        if data['pword'] != data['cpword']:
            flash("Passwords dont match!", "create")
            is_valid = False
        return is_valid