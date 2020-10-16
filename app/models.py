from app import mysql
from flask import flash, current_app
import MySQLdb.cursors
import jwt
from time import time
from app import Config

class User():

    def __init__(self, **kargs):
        for key in kargs:
            setattr(self, key, kargs[key])
        self.is_auth = False
    def is_following(self, followed_id):
        return db.is_following(self.id, followed_id)
    def is_like(self, post_id):
        return db.is_like(self.id, post_id)
    def get_token(self, expires_in = 600):
        return jwt.encode(
            {'reset_password':self.id,
            'exp':time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm= 'HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.get_user('id',id)


from app.database import database as db
