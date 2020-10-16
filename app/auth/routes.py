from app.auth import bp
from app import COOKIE_TIME_OUT
from app.models import User
from app.database import database as db
from flask import request, redirect, url_for, render_template, flash,\
    session , make_response, g
from app.auth.form_validation import Validation
import pyfirmata
import time
from app.auth.email import send_password_reset
from app.main.routes import not_login_req, login_req



@bp.route('/login', methods = ['GET', 'POST'])
@not_login_req
def login():
    if request.method == 'POST' and 'username' in request.form \
        and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        remember = request.form.getlist('inputRemember')
        user = db.check_user(username, password)
        if not user or not user.is_verifyed:
            flash("username or passord incorrect")
            return redirect(url_for('auth.login'))
        session['logedin']= True
        session['user_id'] = user.id
        session['username'] = user.username
        session.permanent = True
        if remember:
            resp = make_response(redirect(url_for('main.index')))
            resp.set_cookie('user_id', str(user.id),max_age = COOKIE_TIME_OUT)
            resp.set_cookie('username', user.username, max_age = COOKIE_TIME_OUT)
            resp.set_cookie('rem', 'checked', max_age = COOKIE_TIME_OUT)
            return resp
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')

@bp.route('/register', methods = ['GET', 'POST'])
@not_login_req
def register():
    if request.method == 'POST' and 'username' in request.form \
        and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if not Validation.is_valid(username , email):
            return redirect(url_for('auth.register'))
        if db.get_user('username', username):
            flash('user name alerady exist')
            return redirect(url_for('auth.register'))
        if db.get_user('email', email):
            flash('email alerady exist')
            return redirect(url_for('auth.register'))
        db.add_user(username, email, password)
        user = db.get_user('username', username)
        send_password_reset(user)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/confirm_registeration/<token>', methods = ['GET'])
@not_login_req
def confirm_registeration(token):
    user = User.verify_token(token)
    if user:
        db.update_state(user.id)
        flash("your registeration confirmed")
    return redirect(url_for('auth.login'))

@bp.route('/logout')
@login_req
def logout():
    session.pop('user_id', None)
    session.pop('logedin', None)
    session.pop('username', None)
    return redirect(url_for('auth.login'))

@bp.route('/reset_password_request', methods = ['GET', 'POST'])
@not_login_req
def reset_password_request():
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        user = db.get_user('email',email)
        if user:
            send_password_reset(user)
        flash('check you email to!!')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html')

@bp.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    user = User.verify_token(token)
    if not user:
        return redirect(url_for('auth.login'))
    if request.method == 'POST' and 'passsource ven word' in request.form \
        and 'confirm_password' in request.form:
        if request.form['password'] == request.form['confirm_password']:
            db.update_password(user.id,request.form['password'])
            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.reset_password' , token = token))
    return render_template('auth/reset_password.html', token = token)
