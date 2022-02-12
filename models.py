from run import db
from run import login_manager
from flask_login import UserMixin
from run import bcrypt


class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255))
    heading = db.Column(db.String(255))
    description = db.Column(db.String(255))
    posted = db.Column(db.Date)
    owner = db.Column(db.String(255))

    def __init__(self, category, heading, description, posted, owner):
        self.category_id = category
        self.heading = heading
        self.description = description
        self.posted = posted
        self.owner = owner


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_names = db.Column(db.String(255))
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, full_names, email, username, password):
        self.full_names = full_names
        self.email = email
        self.username = username
        self.password = password

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password = pwhash.decode('utf8')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(255))
    desc = db.Column(db.String(255))

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
