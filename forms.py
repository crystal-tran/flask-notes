from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Email


class RegisterForm(FlaskForm):
    '''Form for user registration'''

# most important data should be higher up. Move username, password higher up
# TODO: bump username, password, email up
# TODO: enforce constraints in the front-end, add length constraints(min, max)
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
        # TODO: remove datarequired and inputrquired. Redundant?
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
    """Form just for CSRF Protection."""