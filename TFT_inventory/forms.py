from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    email = StringField('email', validators= [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    submit_button = SubmitField()
