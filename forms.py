from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address', validators=[InputRequired(), Email()])
    username = StringField('Enter your username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError("The username already exists")


class LoginForm(FlaskForm):
    username = StringField("Your email address", validators=[InputRequired()])
    password = PasswordField("Your password:", validators=[InputRequired()])
    submit = SubmitField("Sign In")
