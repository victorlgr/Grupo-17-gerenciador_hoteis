from flask_testing import TestCase
from app import app, db, bcrypt
from app.models import User


class TesteBase(TestCase):
    def create_app(self):
        app.config.from_object('app.configuration.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        pwd = bcrypt.generate_password_hash('1234')
        admin = User(name='nome', password=pwd, profile='admin', email='admin@admin.com', password_confirmation=pwd,
                     hotel_id=None)
        db.session.add(admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
