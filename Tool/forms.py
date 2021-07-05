from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField , TextAreaField , FileField , IntegerField , RadioField , DateField
from wtforms.validators import DataRequired, Email , EqualTo, Length
from flask_wtf.file import FileField,FileAllowed
from wtforms import ValidationError

from flask_login import current_user
from Tool.models import User , TeamA, TeamB


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match'), Length(min = 8, max=16)])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email you chose has already been registered')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username yuo chose has already been registered')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log inn')

class TeamsAddForm(FlaskForm):
    teama = StringField('Team A', validators=[DataRequired()])
    teamb = StringField('Team B', validators=[DataRequired()])
    date = DateField('When will event start' , format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
