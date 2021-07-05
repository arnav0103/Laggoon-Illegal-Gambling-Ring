from Tool import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

worka = db.Table('worka',
  db.Column('user_id', db.Integer , db.ForeignKey('users.id')),
  db.Column('teama_id', db.Integer , db.ForeignKey('teama.id')))

workb = db.Table('workb',
  db.Column('user_id', db.Integer , db.ForeignKey('users.id')),
  db.Column('teamb_id', db.Integer , db.ForeignKey('teamb.id')))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String , unique = True)
    password_hash = db.Column(db.String(128))

    teama = db.relationship('TeamA' , secondary = worka , backref = db.backref('supporter', lazy = 'dynamic'))
    teamb = db.relationship('TeamB' , secondary = workb , backref = db.backref('supporter', lazy = 'dynamic'))

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __init__(self, username, password ):
        self.username = username
        self.password_hash = generate_password_hash(password)

class TeamA(db.Model):
    __tablename__ = 'teama'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    a_date = db.Column(db.DateTime,nullable=True,default=datetime.now)

    def __init__(self,name):
        self.name = name

class TeamB(db.Model):
    __tablename__ = 'teamb'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)

    def __init__(self,name):
        self.name = name
