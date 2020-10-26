from app import mysql
import MySQLdb.cursors
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import g

class database():
    @staticmethod
    def add_user(username, email, password):
        hash_pass = generate_password_hash(password)
        cursor = g.dbconx.cursor()
        cursor.execute("""INSERT INTO User (username, password, email, is_verifyed)
                        VALUES (%s,%s,%s,%s)""",(username, hash_pass, email, False))
        g.dbconx.commit()
        cursor.close()

    @staticmethod
    def get_user(row, value):
        cursor = g.dbconx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE {} = %s'.format(row) , (value,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return User(**result)
        return None
    
    @staticmethod
    def check_user(username, password):
        user = database.get_user('username',username)
        if not user or not check_password_hash(user.password, password):
            return None
        return user
    
    @staticmethod
    def update_password(id, password):
        hash_pass = generate_password_hash(password)
        cursor = g.dbconx.cursor()
        cursor.execute('UPDATE user SET password = %s WHERE id = %s',
                        (hash_pass,id))
        g.dbconx.commit()
        cursor.close()
    
    @staticmethod
    def update_state(id):
        cursor = g.dbconx.cursor()
        cursor.execute('UPDATE User SET is_verifyed = %s WHERE id = %s',
                        (1,id))
        g.dbconx.commit()
        cursor.close()
    
    @staticmethod
    def add_post(id, body):
        cursor = g.dbconx.cursor()
        cursor.execute("""INSERT Post (user_id,body)
                        VALUES (%s,%s)""",(id, body))
        g.dbconx.commit()
        cursor.close()
    @staticmethod
    def update_post(id, body):
        cursor = g.dbconx.cursor()
        cursor.execute("""UPDATE Post SET body = %s
                         WHERE id = %s""",(body, id))
        g.dbconx.commit()
        cursor.close()
    
    @staticmethod
    def get_user_posts(id):
        cursor = g.dbconx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(""" SELECT username AS author ,Post.id,Likes, body  FROM Post INNER JOIN
                        User ON Post.user_id = User.id WHERE User.id = %s
                        ORDER BY Post.creation_time DESC""", (id,))
        posts = cursor.fetchall()
        cursor.close()
        return posts
    
    @staticmethod
    def update_user_profile(id, username, about_me):
        cursor = g.dbconx.cursor()
        cursor.execute(""" UPDATE User SET username = %s, about_me = %s
                        WHERE id = %s""",(username, about_me, id))
        g.dbconx.commit()
        cursor.close()
    
    @staticmethod
    def follow_user(follower_id, followed_id):
        cursor = g.dbconx.cursor()
        cursor.execute(""" INSERT INTO Follower (follower_id, followed_id)
                        VALUES (%s, %s)""", (follower_id, followed_id))
        g.dbconx.commit()
        cursor.close()
    
    @staticmethod
    def unfollow_user(follower_id, followed_id):
        cursor = g.dbconx.cursor()
        cursor.execute(""" DELETE FROM Follower WHERE
            follower_id = %s AND followed_id = %s""", (follower_id, followed_id))
        g.dbconx.commit()
        cursor.close()
    
    @staticmethod
    def is_following(follower_id, followed_id):
        cursor = g.dbconx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM Follower WHERE follower_id = %s
                        AND followed_id = %s""",(follower_id, followed_id))
        res = cursor.fetchone()
        cursor.close()
        if res:
            return True
        return False
    @staticmethod
    def add_comment(post_id, user_id):
        cursor = g.dbconx.cursor()
        cursor.execute("""INSERT INTO Comment (post_id, user_id)
                VALUES(%s, %s)""", (post_id, user_id))
        g.dbconx.commit()
        cursor.close()
    
    @staticmethod
    def add_like(post_id, user_id):
        cursor = g.dbconx.cursor()
        try:
            cursor.execute("""INSERT INTO Likes (post_id, user_id)
                    VALUES(%s, %s)""", (post_id, user_id))
        except MySQLdb.Error as e:
            print(e)
            return None
        try:
            g.dbconx.commit()
        except MySQLdb.Error as e:
            print(e)
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def is_like(user_id, post_id):
        cursor = g.dbconx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM Likes WHERE user_id = %s
                        AND post_id = %s""",(user_id, post_id))
        res = cursor.fetchone()
        cursor.close()
        if res:
            return True
        return False