from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

# Adding Flask Security of passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import Secrets Module
import secrets

# Import LoginManager & UserMixin (help login userrs & store their credentials)
from flask_login import UserMixin, LoginManager

# Import Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # Create relationship between User table and TFT table

    def __init__(self, email, username, password, first_name = '', last_name = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)

    def __repr__(self):
        return f"User {self.email} has been added to our Database!"

class Champion(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    skill = db.Column(db.String(200), nullable = False)
    skill_description = db.Column(db.String(200), nullable = False)
    cost = db.Column(db.Numeric(precision=10, scale=2))
    traits = db.Column(db.String(150), nullable=False)
    series = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, skill, skill_description, cost, traits, series, user_token):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.skill = skill
        self.skill_description = skill_description
        self.cost = cost
        self.traits = traits
        self.series = series
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Champion {self.name} has been added to the database!"

class ChampionSchema(ma.Schema):
    class Meta:
        fields = ['id','name','description','skill','skill_description','cost','traits','series']

champion_schema = ChampionSchema()
champions_schema = ChampionSchema(many = True)

