from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(500))
    password = db.Column(db.String(500))
    password_confirmation = db.Column(db.String(500))
    profile = db.Column(db.String(15))
    email = db.Column(db.String(120), unique = True)
    # posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r %r>' % (self.name, self.password)

    def __init__(self, name, password, password_confirmation, profile, email):
        self.name = name
        self.password = password
        self.password_confirmation = password_confirmation
        self.profile = profile
        self.email = email
