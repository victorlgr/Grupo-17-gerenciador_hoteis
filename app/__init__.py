from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

app = Flask(__name__)

#Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('configuration.ProductionConfig')
app.config.from_object('app.configuration.DevelopmentConfig')
#app.config.from_object('configuration.TestingConfig')

bs = Bootstrap(app) #flask-bootstrap
db = SQLAlchemy(app) #flask-sqlalchemy
migrate = Migrate(app, db)
bcrypt = Bcrypt()
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"
login_manager.login_message_category = "info"

@app.before_first_request
def create_tables():
    db.create_all()


from app import views, models