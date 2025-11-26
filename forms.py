from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.validators import Email




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('confirm-password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class JobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    short_description = StringField('Short Description', validators=[DataRequired(), Length(max=200)])
    long_description = StringField('Long Description', validators=[DataRequired(), Length(max=200)])
    company = StringField('Company', validators=[DataRequired(), Length(max=150)])
    location = StringField('Location', validators=[DataRequired(), Length(max=150)])
    salary = IntegerField('Salary', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired(), Length(max=150)])
    submit = SubmitField('Add Vacancy')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image = FileField('profile image')
    submit = SubmitField('Update Account')