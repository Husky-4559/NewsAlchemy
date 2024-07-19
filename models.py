# cSpell:ignore sqlalchemy jsonify wtforms newsalchemyuser yourpassword

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)

    def __init__(self, user_id, title, url):
        self.user_id = user_id
        self.title = title
        self.url = url

    def __repr__(self):
        return f'<Favorite {self.title}>'