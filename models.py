"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

DEFAULT_IMG_URL = 'https://image.flaticon.com/icons/png/128/1077/1077114.png'

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMG_URL)

    @property
    def full_name(self):
        """Full name of user"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref="posts")

    @property
    def post_date(self):
        """formatted date"""

        # Formatting a datetime
        # dt.strftime("%A, %d. %B %Y %I:%M%p")
        #'Tuesday, 21. Novemeber 2006 04:30PM'

        return self.created_at.strftime("%a, %d. %b %Y %I:%M%p")



