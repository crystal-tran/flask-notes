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

