from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField, validators
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo, Length, URL

class RegisterForm(FlaskForm):
    username = StringField("Username", [InputRequired, validators.Length(min=4, max=25)])
    password = PasswordField("Passwword", [InputRequired, validators.Length(min=8)])
    submit = SubmitField("")

class LoginForm(FlaskForm):
    username = StringField("Username", [InputRequired, validators.Length(min=4, max=25)])
    password = PasswordField("Passwword", [InputRequired, validators.Length(min=8)])
    submit = SubmitField("")