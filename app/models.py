from app import db
from flask_login import UserMixin
from datetime import datetime as dt


class Hotels(db.Model):
    __tablename__ = 'Hotels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(30))
    cnpj = db.Column(db.String(25))
    user_id = db.Column(db.Integer)
    address_id = db.Column(db.Integer, db.ForeignKey('Addresses.id'))
    created_at = db.Column(db.DateTime, default=dt.now())


class Rooms(db.Model):
    __tablename__ = 'Rooms'
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('Hotels.id'))
    number = db.Column(db.Integer)
    name = db.Column(db.String(30))
    kind = db.Column(db.String(15))
    phone_extension = db.Column(db.String(15))
    price = db.Column(db.REAL)
    guest_limit = db.Column(db.Integer)
    status = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=dt.now())


class Addresses(db.Model):
    __tablename__ = 'Addresses'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(30))
    neighborhood = db.Column(db.String(25))
    city = db.Column(db.String(25))
    state = db.Column(db.String(20))
    country = db.Column(db.String(20))
    zip_code = db.Column(db.String(10))
    number = db.Column(db.String(10))
    complement = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=dt.now())

class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('Hotels.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('Addresses.id'))
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    cpf = db.Column(db.String(15))
    birthday = db.Column(db.DateTime)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    password = db.Column(db.String(500))
    password_confirmation = db.Column(db.String(500))
    profile = db.Column(db.String(15))
    email = db.Column(db.String(120), unique=True)
    hotel_id = db.Column(db.Integer)
    # posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_profile(self):
        return self.profile

    def get_hotel_id(self):
        return self.hotel_id

    def __repr__(self):
        return '<User %r %r>' % (self.name, self.password)

    def __init__(self, name, password, password_confirmation, profile, email, hotel_id):
        self.name = name
        self.password = password
        self.password_confirmation = password_confirmation
        self.profile = profile
        self.email = email
        self.hotel_id = hotel_id

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))
    total_guests = db.Column(db.Integer)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    payment_type = db.Column(db.String(20)) #Enum?
