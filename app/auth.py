import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# authentification

@bp.route('/register', methods=('GET', 'POST'))
def register():
    '''
    Gets the reguest from /auth/register and calls register
    POST
        if the user is submitted start validating input
    Input
        - the user name 
        - the user password
    Validation
        - not empty
    If validation succeeds insert the new user data to the dB
    After
        - redirect to the login page
    Flash() 
        - store messsages to be retrieved in the event an error is raised
    
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


# login

@bp.route('/login', methods=('GET', 'POST'))
def login():
    '''
    Fetchone()
        - returns one row from the dB with the given username
        - if no return None
    hash the data the same way as stored in the dB
    Store a session (cookie)
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# logged in user 
@bp.before_app_request
def load_logged_in_user():
    '''
    Registers a function that runs before the view function
         no matter what URL is requested
    load_logged_in_user 
       - checks if a user id is stored in the session
       - gets that user data from the database, storing it on g.user
    return:
       if no user id g.user = None
    '''
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    '''
    remove the user id from the current session(cookies)
    '''
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    '''
    login_required
        ensures that the Users are logged in 
        this involves creating a decorator to secure views
    Because editing of interests needs users to be logged in
    '''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view