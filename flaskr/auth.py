import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash #Password stuff

from flaskr.db import get_db 

bp = Blueprint('auth', __name__, url_prefix='/auth') #Register blueprint

@bp.route('/register', methods=('GET', 'POST')) # route from blue print

# Registration form
def register():
    if request.method == 'POST': #Do you want to POST method
        username = request.form['username']
        password = request.form['password']
        db = get_db()  # Get and open DB
        error = None # This holds any error statement

        if not username:
            error = 'Username is required.' # Assure that username is present
        elif not password:
            error = 'Password is required.' # Assures that password is present
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None: # Assure that a user being registered is unique
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password)) # Register user with hashed password
            )
            db.commit()
            return redirect(url_for('auth.login')) # Finish registering user

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password']
        db = get_db()
        error = None # Stores any error
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() 

        if user is None:
            error = 'Incorrect username.' # Give error for username
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.' # Give error for password

        if error is None:
            session.clear() #Clear session and more session stuff. It's a dict. It stores the data in a cookie that is sent to the browser.
            session['user_id'] = user['id']
            return redirect(url_for('index')) #Login

        flash(error) # Show error

    return render_template('auth/login.html') #Render template

@bp.before_app_request # Runs before view template loads, and it checks if the session has a logged in user
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear() # Logs out by clearing session, so load_logged_in_user doesn't log them in again
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view) #Has a new view function that wraps the original view it's applied to. The new function checks if a user is loaded and redirects to the login page. This decorator will be used for blog views
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
