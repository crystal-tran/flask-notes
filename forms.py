from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, ValidationError

def whitespace_check(form, field):
    if len(field.data.strip()) == 0:
        raise ValidationError('Field must not contain only whitespace')

class RegisterForm(FlaskForm):
    '''Form for user registration'''

    username = StringField(
        'Username:',
        validators=[InputRequired(), Length(3, 20), whitespace_check],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(3, 30)],
    )

    email = StringField(
        'Email:',
        validators=[Email(), Length(3, 50)],
    )

    first_name = StringField(
        'First Name:',
        validators=[InputRequired(), Length(1, 100)],
    )

    last_name = StringField(
        'Last Name:',
        validators=[InputRequired(), Length(1, 100)],
    )


class LoginForm(FlaskForm):
    '''Form for logging in a user.'''

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(3, 20)],
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(3, 30)],
    )

class NoteForm(FlaskForm):
    '''Form for adding a note.'''

    title = StringField(
        "Title",
        validators=[InputRequired()]
    )

    content = StringField(
        "Content",
        validators=[InputRequired()]
    )


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection."""