from email.policy import default
from turtle import title
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/img/49468"

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(25), nullable = False)
    last_name = db.Column(db.String(25), nullable = False)
    image_URL = db.Column(db.String, nullable = False, default = DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def easily_read_date(self):
        """outputs an easy to read date"""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
        # %a is abbreviated day, %b is abbreviated month, %-d is day of month as decimal (1, 2, 3...), %Y is full 4 number year, %-I is hour number, %M is minute number with a 0 in front of it for the first number, %p is AM or PM


def connect_db(app):
    """connects this database to provided Flask app, needs to be called in app"""

    db.app = app
    db.init_app(app)
    # don't understand this

