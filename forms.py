from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Email


class RegisterForm(FlaskForm):
    '''Form for user registration'''

    first_name = StringField(
        'First Name:',
        validators=[InputRequired(), DataRequired()]
    )

    last_name = StringField(
        'Last Name:',
        validators=[InputRequired(), DataRequired()]
    )

    email = StringField(
        'Email:',
        validators=[InputRequired(), DataRequired(), Email()],
    )

    username = StringField(
        'Username:',
        validators=[InputRequired(), DataRequired()],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), DataRequired()],
    )



class LoginForm(FlaskForm):
    '''Form for logging in a user.'''

    username = StringField(
        "Username",
        validators=[InputRequired(), DataRequired()],
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), DataRequired()],
    )

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""