from flask import flash
import re

class Validation():
    def is_valid(username,email):
        result = 1
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('email not valid')
            result = 0
        if not re.match(r'[A-Za-z0-9]+', username):
            flash('username not valid')
            result = 0
        return result