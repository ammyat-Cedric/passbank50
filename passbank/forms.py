from flask_wtf import FlaskForm
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.form import Form
from wtforms.validators import Email, InputRequired, ValidationError, input_required
from passbank.models import Users

class RegisterationForm(Form):
  username  = StringField('Username', validators=[validators.input_required(), validators.Length(min=5, max=20)])
  email =  StringField('Email', validators=[validators.input_required(), Email()])
  password = PasswordField('Password', validators=[validators.input_required()])
  confirm_password = PasswordField('Comfirm Password', validators=[validators.input_required(), validators.EqualTo('password')])
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = Users.query.filter_by(username = username.data).first()
    if user:
      raise ValidationError('Username already existed!')

  def validate_email(self, email):
    user = Users.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('That email is already existed!')


class LoginForm(Form):
  email = StringField('Email', validators=[validators.input_required(),Email()])
  password = PasswordField('Password', validators=[validators.input_required()])
  submit = SubmitField('Log In')


class UpdateAccountForm(Form):
  username = StringField('New Username', validators=[validators.Length(min=5, max=20)])
  email = StringField('New Email', validators=[Email()])
  new_password = PasswordField('New Password')
  current_password = PasswordField('Current Password', validators=[
                           validators.input_required()])
  submit = SubmitField('Update')

  def validate_username(self, username):
    if username.data != current_user.username:
      user = Users.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('Username already existed!')

  def validate_email(self, email):
    if email.data != current_user.email:
      user = Users.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('That email is already existed!')

