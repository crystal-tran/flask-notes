import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import User, connect_db, db, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, NoteForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

USERNAME_KEY = 'username'

@app.get('/')
def homepage():
    """Redirect user to register page."""

    return redirect("/register")


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Show registration form and register user upon form submission'''

    form = RegisterForm()

    if form.validate_on_submit():
        input_data = {k: v for k, v in form.data.items() if k != "csrf_token"}

        username_email_is_valid = User.validate_username_and_email(
            input_data['username'],input_data['email'])

        if username_email_is_valid:
            new_user = User.register(**input_data)

            db.session.commit()
            session[USERNAME_KEY] = new_user.username

            flash('User registered!')
            return redirect(f'/users/{new_user.username}')

        else:
            form.username.errors = ["Username/email already exists"]

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Show form to login a user and process login form'''

    if USERNAME_KEY in session:

        flash("You're already logged in!.")
        return redirect(f'/users/{session[USERNAME_KEY]}')

    form = LoginForm()

    if form.validate_on_submit():
        login_data = {k: v for k, v in form.data.items() if k != "csrf_token"}

        user = User.authenticate(**login_data)

        if user:
            session[USERNAME_KEY] = user.username

            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad username/password"]

    return render_template('login.html', form=form)


@app.get('/users/<username>')
def show_users(username):
    '''Show data for logged in user or redirects if username
    does not match username on page
    Raise unauthorized error if not logged in or invalid username'''

    if 'username' not in session or session[USERNAME_KEY] != username:
        raise Unauthorized

    user = User.query.get_or_404(username)

    form = CSRFProtectForm()

    return render_template(
        'users.html',
        user=user,
        form=form,
    )


@app.post('/logout')
def logout():
    '''Logout user and redirects to homepage
    Raise unauthorized error if invalid csrf token'''

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(USERNAME_KEY, None)
        return redirect('/')

    else:
        raise Unauthorized

@app.route('/users/<username>/notes/add', methods=['GET','POST'])
def add_note(username):
    '''Add a note for a user'''

    if 'username' not in session or session[USERNAME_KEY] != username:
        raise Unauthorized

    user = User.query.get_or_404(username)
    form = NoteForm()

    if form.validate_on_submit():
        note_data = {k: v for k, v in form.data.items() if k != "csrf_token"}

        note = Note(owner_username=username, **note_data)

        db.session.add(note)
        db.session.commit()

        return redirect(f'/users/{username}')

    else:
        return render_template("notes.html",
                               form=form,
                               user=user)

