from flask import render_template, request, redirect, url_for, abort
from run import db
from run import app
from run import bcrypt
from models import *
from datetime import date
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm

from flask_mail import Message
from run import mail
from uuid import uuid1
import os
import requests, json

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def get_blogs():
    blogs = Blog.query.all()
    request = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    response = json.loads(request.content)
    return render_template('blogs.html', blogs=blogs, response=response)


@app.route('/my-blogs')
def my_blogs():
    blogs = Blog.query.filter_by(owner=current_user.username)
    message = ''
    if not blogs:
        message = "You have not uploaded any blog"
    return render_template('my_blogs.html', blogs=blogs)


# def mail_message(subject,template,to,**kwargs):
#     sender_email = 'joshua.barawa@student.moringaschool.com'
#
#     email = Message(subject, sender=sender_email, recipients=[to])
#     email.body= render_template(template + ".txt",**kwargs)
#     email.html = render_template(template + ".html",**kwargs)
#     mail.send(email)


@app.route('/blog-form')
@login_required
def form_pitch():
    return render_template('blog_form.html')


@app.route('/blogs/<string:category_name>')
def get_blogs_by_category(category_name):
    blogs = Blog.query.filter_by(category_name=category_name)
    request = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    response = json.loads(request.content)
    return render_template('blogs.html', blogs=blogs, response=response)


@app.route('/post-blog', methods=['POST'])
@login_required
def add_blog():

    if request.method == 'POST':
        category = request.form['category']
        image = request.files['photo']
        heading = request.form['heading']
        description = request.form['description']
        posted = date.today()
        owner = current_user.username
        pic_filename = secure_filename(image.filename)
        pic_name = str(uuid1()) + "_" + pic_filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

        if category == '---select category---' or description == '' or heading == '':
            return render_template("blog_form.html", message="Please enter required fields")
        else:
            blog = Blog(category_name=category, image=pic_name, heading=heading, description=description, posted=posted, owner=owner)
            db.session.add(blog)
            db.session.commit()
            return redirect(url_for("get_blogs"))


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(register_form.password.data).decode('utf8')
        user = User(full_names=register_form.full_names.data, email=register_form.email.data, username=register_form.username.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        send_mail(register_form.email.data)
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=register_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, login_form.password.data):
                login_user(user)
                print(current_user)
                return redirect(url_for("get_blogs"))
    return render_template('auth/login.html', form=login_form)


@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first()
    if user is None:
        abort(404)
    return render_template("profile.html", user=user)


@app.route('/blog/<int:id>')
@login_required
def read_more(id):
    blog = Blog.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(blog_id=id)
    if blog is None:
        abort(404)
    return render_template("readmore.html", blog=blog, comments=comments)


@app.route('/add-comment', methods=['POST'])
@login_required
def add_comment():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['comment']
        blog_id = request.form['blog_id'];
        if name == '' or description == '' :
            return render_template("readmore.html", message="Please enter required fields")
        else:
            comment = Comment(blog_id, name, description)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for("read_more", id=blog_id))


@app.route('/delete-comment/<int:id>')
@login_required
def delete_comment(id):
    delete_comment = Comment.query.filter_by(id=id).first()
    db.session.delete(delete_comment)
    db.session.commit()
    return redirect(url_for("read_more", id=delete_comment.blog_id))


@app.route('/blog-update/<int:id>')
@login_required
def blog_update_form(id):
    blog = Blog.query.filter_by(id=id).first()
    return render_template("blog_update.html", blog=blog)


@app.route('/update-blog/<int:id>', methods=['POST'])
@login_required
def blog_update(id):
    category = request.form['category']
    image = request.files['photo']
    heading = request.form['heading']
    description = request.form['description']
    posted = date.today()
    owner = current_user.username
    pic_filename = secure_filename(image.filename)
    pic_name = str(uuid1()) + "_" + pic_filename
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

    edited_blog = Blog.query.filter_by(id=id).update({"category_name":category, "image":pic_name, "heading":heading,
                                                       "description":description, "posted":posted, "owner":owner})

    db.session.commit()
    return redirect(url_for("my_blogs"))


@app.route('/delete-blog/<int:id>')
@login_required
def delete_blog(id):
    delete_blog = Blog.query.filter_by(id=id).first()
    db.session.delete(delete_blog)
    db.session.commit()
    return redirect(url_for("my_blogs"))


def send_mail(recipient):
    msg = Message(
        'Subscription',
        sender='mwamlandabarawa@gmail.com',
        recipients=[recipient]
    )
    msg.body = 'Hello, \n You have subscribed to our daily messaging.' \
               ' You will receive the best movie recommendations'
    mail.send(msg)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))