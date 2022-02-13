from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import InputRequired, Email, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    profile_pic = FileField('Profile Pic')
    full_names = StringField("Enter your names", validators=[InputRequired()])
    email = StringField('Your Email Address', validators=[InputRequired(), Email()])
    username = StringField('Enter your username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError("The username already exists")

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError("The email already exists")


class LoginForm(FlaskForm):
    username = StringField("Enter username address", validators=[InputRequired()])
    password = PasswordField("Enter password:", validators=[InputRequired()])
    submit = SubmitField("Sign In")
