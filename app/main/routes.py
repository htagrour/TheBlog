from flask import redirect, render_template, session, url_for,\
    g, flash, request, jsonify, abort
from app.main import bp
from app import mysql
from app.database import database as db
from app.models import User
from functools import wraps

def login_req(func):
    @wraps(func)
    def decorated_function(*args, **kargs):
        if not g.user or not g.user.is_auth:
            flash('you should login')
            return redirect(url_for('auth.login'))
        return func(*args, **kargs)
    return decorated_function

def not_login_req(func):
    @wraps(func)
    def decorated_function(*args, **kargs):
        if g.user and g.user.is_auth:
            return redirect(url_for('main.index'))
        return func(*args, **kargs)
    return decorated_function

@bp.before_app_request
def before_request():
    if not hasattr(g, 'dbconx'):
        g.dbconx = mysql.connect
    if 'user_id' in session:
        user = db.get_user('id',session['user_id'])
        if user:
            user.is_auth = True
    else:
        user = User()
    g.user = user

@bp.teardown_app_request
def teardown(ex):
    if hasattr(g, 'dbconx'):
        conx = g.dbconx
        conx.close


@bp.route('/', methods = ['GET', 'POST'])
@bp.route('/index', methods = ['GET', 'POST'])
@login_req
def index():
    if request.method == 'POST' and 'body' in request.form:
        db.add_post(g.user.id, request.form['body'])
    posts = db.get_user_posts(g.user.id)
    return render_template('index.html', title = 'welcome', posts = posts)

@bp.route('/user/<username>', methods = ['GET', 'POST'])
def user(username):
    user = db.get_user('username', username)
    if not user:
        abort(404)
    posts = db.get_user_posts(user.id)
    return render_template('user.html', user = user, posts= posts)

@login_req
@bp.route('/edit_profile/' , methods = ['GET', 'POST'])
def edit_profile():

    if request.method == 'POST' and 'username' in request.form\
        and 'about_me' in request.form:
        _username = request.form['username']
        _about_me = request.form['about_me']
        if db.get_user('username', _username) and _username != g.user.username:
            flash('username alredy exist')
            return redirect(url_for('main.edit_profile', username = username))
        db.update_user_profile(g.user.id, _username, _about_me)
        return redirect(url_for('main.edit_profile'))
    return render_template('edit_profile.html', username = g.user.username,
                            about_me = g.user.about_me)

@bp.route('/follow/<username>', methods = ['GET', 'POST'])
@login_req
def follow(username):
    user = db.get_user('username', username)
    if not user:
        flash('User {} not exist'.format(username))
        return redirect(url_for('main.index'))
    db.follow_user(g.user.id, user.id)
    return redirect(redirect(url_for('main.user', username = username)))

@bp.route('/unfollow/<username>', methods = ['GET', 'POST'])
@login_req
def unfollow(username):
    user = db.get_user('username', username)
    if not user:
        flash('User {} not exist'.format(username))
        return redirect(url_for('main.index'))
    db.unfollow_user(g.user.id, user.id)
    return redirect(redirect(url_for('main.user', username = username)))

@bp.route('/like_post/<post_id>', methods = ['GET', 'POST'])
@login_req
def like_post(post_id):
    if (not g.user.is_like):
        db.add_like(post_id, g.user.id)
    return redirect (url_for('main.index'))
