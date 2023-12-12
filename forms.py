from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Email


class RegisterForm(FlaskForm):
    '''Form for user registration'''

    username = StringField(
        'Username:',
        validators=[InputRequired(), DataRequired()],
    )

    email = StringField(
        'Email:',
        validators=[InputRequired(), DataRequired(), Email()],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), DataRequired()],
    )

    first_name = StringField(
        'First Name:',
        validators=[InputRequired(), DataRequired()]
    )

    last_name = StringField(
        'Last Name:',
        validators=[InputRequired(), DataRequired()]
    )


class LoginForm(FlaskForm):
    '''Form for logging in a user.'''

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = StringField(
        "Password",
        validators=[InputRequired()]
    )

