from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    email = StringField('email', validators= [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    submit_button = SubmitField()

class ChampionForm(FlaskForm):
    name = StringField('name')
    description = StringField('description')
    skill = StringField('skill')
    skill_description = StringField('skill description')
    cost = DecimalField('cost')
    traits = StringField('traits')
    series = StringField('series')
    champion_info = StringField('champion info')
    submit_button = SubmitField()