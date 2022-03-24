# Classes SQL
from app import db
from datetime import datetime as dt


class Hotels(db.Model):
    __tablename__ = 'Hotels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    phone = db.Column(db.String(20))
    address_id = db.Column(db.Integer, db.ForeignKey('Addresses.id'))
    user_id = db.Column(db.Integer)
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
    complement = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=dt.now())
