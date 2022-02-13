from flask import render_template, request, redirect, url_for, abort
from run import app
from models import Blog, User, Comment
from datetime import date
from run import db
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm
from run import bcrypt
from flask_mail import Message
from run import mail


def mail_message(subject,template,to,**kwargs):
    sender_email = 'joshua.barawa@student.moringaschool.com'

    email = Message(subject, sender=sender_email, recipients=[to])
    email.body= render_template(template + ".txt",**kwargs)
    email.html = render_template(template + ".html",**kwargs)
    mail.send(email)


@app.route('/pitch-form')
def form_pitch():

    categories = Category.query.all()
    return render_template('pitch_form.html', categories=categories)


@app.route('/')
def get_all_pitches():
    pitches = Pitch.query.all()
    return render_template('pitches.html', pitches=pitches)


@app.route('/<int:id>')
def get_pitches_by_category(id):
    pitches = Pitch.query.filter_by(category_id=id)
    return render_template('pitches.html', pitches=pitches)


@app.route('/add-pitch', methods=['POST'])
@login_required
def add_pitch():

    categories = Category.query.all()
    if request.method == 'POST':
        category = request.form['category']
        heading = request.form['name']
        description = request.form['pitch']
        posted = date.today()
        upvote = 0
        downvote = 0
        name = current_user.username;

        if category == '---select category---' or description == '' or heading == '':
            return render_template("pitch_form.html", message="Please enter required fields", categories=categories)
        else:
            pitch = Pitch(category, heading, description, posted, upvote, upvote,name)
            db.session.add(pitch)
            db.session.commit()
            return redirect(url_for("get_all_pitches"))


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(register_form.password.data).decode('utf8')
        user = User(email=register_form.email.data, username=register_form.username.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
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
                return redirect(url_for("get_all_pitches"))
    return render_template('auth/login.html', form=login_form)


@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first()
    if user is None:
        abort(404)
    return render_template("profile.html", user=user)


@app.route('/pitch/<int:id>')
@login_required
def comment(id):
    pitch = Pitch.query.filter_by(id=id).first()
    comments = Comment.query.all()
    if pitch is None:
        abort(404)
    return render_template("readmore.html", pitch=pitch, comments=comments)


@app.route('/add-comment', methods=['POST'])
@login_required
def add_comment():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['comment']

        if name == '' or description == '' :
            return render_template("readmore.html", message="Please enter required fields")
        else:
            comment = Comment(name, description)
            db.session.add(comment)
            db.session.commit()
            return render_template("success.html", message="Comment was added successful")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))