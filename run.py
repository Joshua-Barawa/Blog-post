from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

import os

app = Flask(__name__)

ENV = os.environ.get("ENV")

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://blogdb:hello@localhost/blogdb'
app.config['SECRET_KEY'] = "1234567"
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from views import *

manager = Manager(app)
manager.add_command('server', Server)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return None


login_manager.login_view = 'login'

bcrypt = Bcrypt(app)
mail = Mail(app)

from models import *


@manager.shell
def make_shell_context():
    return dict(db=db, app=app)


if __name__ == '__main__':
    manager.run()
