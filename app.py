import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import User, connect_db, db
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.get('/')
def homepage():
    """Redirect user to register page"""

    return redirect("/register")

# create routes for get & post/register

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Register user upon form submission & show registration form'''

    form = RegisterForm()

    if form.validate_on_submit():
        input_data = {k: v for k, v in form.data.items() if k != "csrf_token"}

        new_user = User.register(**input_data)

        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username

        flash('User registered!')

        return redirect(f'/users/{new_user.username}')

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Show form to login a user and process login form'''

    form = LoginForm()

    if form.validate_on_submit():
        login_data = {k: v for k, v in form.data.items() if k != "csrf_token"}

        user = User.authenticate(**login_data)

        if user:
            session['username'] = user.username

            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad username/password"]
            # TODO: Question to ask duriong code review.

    return render_template('login.html', form=form)



@app.get('/users/<username>')
def show_users(username):
    '''Show data for a logged in user'''

    user = User.query.get_or_404(username)

    if 'username' not in session:

        flash('Log in is required for user info.')
        return redirect('/login')

    # make sure user logged in matches page being accessed
    elif session['username'] != user.username:

        logged_in_username = session['username']

        flash('Unable to view other info for other users!')
        return redirect(f"/users/{logged_in_username}")

    form = CSRFProtectForm()

    return render_template(
        'users.html',
        user=user,
        form=form,
    )

