from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

import os
app = Flask(__name__)

ENV = 'dev'

if ENV == 'prod':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://blogdb:hello@localhost/blogdb'
    app.config['SECRET_KEY'] = "1234567"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
else:
    app.debug == False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vfcrkuevbauihe:9a05fdafba9e870da60ce663723631402bdb4e5f550c356d49adff45f1cc60ad@ec2-3-212-194-162.compute-1.amazonaws.com:5432/df12jjr7k1aigj'
    app.config['SECRET_KEY'] = "1234567"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


manager = Manager(app)
manager.add_command('server', Server)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)
mail = Mail(app)

from views import *
from models import Blog, User, Comment


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Pitch=Pitch,  Comment=Comment)


if __name__ == '__main__':
    app.run(debug=True)
