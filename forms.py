from unicodedata import name
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional
from flask_wtf import FlaskForm



class LoginForm(FlaskForm):
    username = StringField("username",validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email",validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("title",validators=[InputRequired()])
    content = StringField("content",validators=[InputRequired()])
