from run import db
from flask_login import UserMixin
from run import bcrypt


class Blog(db.Model):
    __tablename__ = "blogs"
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255))
    image = db.Column(db.Text)
    heading = db.Column(db.String(255))
    description = db.Column(db.String(255))
    posted = db.Column(db.Date)
    owner = db.Column(db.String(255))

    def __init__(self, category_name, image, heading,description, posted, owner):
        self.category_name = category_name
        self.image = image
        self.heading = heading
        self.description = description
        self.posted = posted
        self.owner = owner


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_names = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, full_names, email, username, password):
        self.full_names = full_names
        self.email = email
        self.username = username
        self.password = password

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password = pwhash.decode('utf8')


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    name = db.Column(db.String(255))
    desc = db.Column(db.String(255))

    def __init__(self, blog_id, name, desc):
        self.blog_id = blog_id
        self.name = name
        self.desc = desc
