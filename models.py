from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    @classmethod
    def validate_username_and_email(cls, username, email):
        '''Checks if username and email is unique. Returns True/False'''

        user_check = cls.query.filter_by(username=username).one_or_none()
        email_check = cls.query.filter_by(email=email).one_or_none()

        return user_check and email_check

    @classmethod
    def register(cls, username, email, first_name, last_name, password):
        '''Register user with hashed password and return user instance'''

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        user = cls(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=hashed,
        )

        db.session.add(user)

        return user

    @classmethod
    def authenticate(cls, username, password):
        '''Validate that user exists and password is valid

        Return user if valid; else return False.
        '''

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False




