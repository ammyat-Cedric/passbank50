import csv
from io import TextIOWrapper
from flask import redirect, url_for, flash, render_template, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from passbank import app, db, mail
from passbank.models import Users, Password
from passbank.forms import RegisterationForm, LoginForm, UpdateAccountForm, ResetForm, ResetPasswordForm


# FLASK ROUTES
@app.route("/")
@login_required
def dashboard():
  passwords = Password.query.filter_by(owner = current_user)
  has_items = bool(passwords)
  return render_template("dashboard.html", passwords=passwords, has_items=has_items)


@app.route('/add', methods=['GET', 'POST'])
def add():
  return render_template('add.html')

@app.route('/add/website', methods=['POST'])
@login_required
def addWebsite():
  if request.method == 'POST':
    website = request.form.get('website')
    url = request.form.get('url')
    username = request.form.get('username')
    password = request.form.get('password')
    h_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    add_password = Password(website=website, url=url, username=username, password=h_password, owner=current_user)
    db.session.add(add_password)
    db.session.commit()
    flash('Successfully added!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/add/upload', methods=['GET', 'POST'])
@login_required
def upload():
  if request.method == 'POST':
    csv_file = request.files['file']
    csv_file = TextIOWrapper(csv_file, encoding='utf-8')
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    counter = 0

    for row in csv_reader:
      passwords = Password(website=row[0], url=row[1], username=row[2], password=row[3], owner=current_user)
      db.session.add(passwords)
      db.session.commit()
      counter += 1

    flash(f'You have successfully imported {counter} passwords!', 'success')
    return redirect(url_for('dashboard'))
  return redirect(url_for('add'))


@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for("dashboard"))

  form = RegisterationForm(request.form)
  if request.method == 'POST' and form.validate():
    username = form.username.data
    email = form.email.data
    h_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)

    user = Users(username=username, email=email, hash=h_password)
    db.session.add(user)
    db.session.commit()
    flash('You account is successfully created. You are able to login.', 'success')
    return redirect(url_for("login"))

  return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("dashboard"))

  form = LoginForm(request.form)
  if request.method == 'POST' and form.validate():
    email = form.email.data
    password = form.password.data

    user = Users.query.filter_by(email=email).first()
    if user and check_password_hash(user.hash, password):
      login_user(user, remember=False)
      next_page = request.args.get('next')
      flash('You have successfully logged in.', 'success')
      return redirect(next_page) if next_page else redirect(url_for("dashboard"))
    elif not user:
      flash('There is no user account with this email.')
      return redirect(url_for('register'))
    else:
      flash('Email or password is incorrect.', 'danger')
      return redirect(url_for("login"))

  return render_template('login.html', form=form)


@app.route("/logout")
def logout():
  logout_user()
  flash("You have logged out!", 'info')
  return redirect(url_for("dashboard"))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm(request.form)
  if request.method == 'POST' and form.validate():
    current_password = form.current_password.data

    if not check_password_hash(current_user.hash, current_password):
      flash("Current password is wrong!", 'danger')
      return redirect(url_for("account"))
    else:
      new_username = form.username.data
      new_email = form.email.data
      new_password = form.new_password.data

      if not (new_username, new_email, new_password):
        flash('Provide data to update account!', 'info')
        return redirect(url_for('account'))

      current_user.username = new_username
      current_user.email = new_email

      if new_password:
        h_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        current_user.hash = h_password

      db.session.commit()
      flash("Your account info has been updated!", 'success')
      return redirect(url_for("account"))

  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email

  return render_template("account.html", form=form)

def send_reset_email(user):
  token = user.get_reset_token()
  body = f'''To reset your password, visit the following link: 
  
{url_for('reset_token', token=token, _external=True)}

Caution: After 30 minutes, this link will be invalid.

If you did not make this request then simply ignore this email and no change will be made!!
'''
  msg = Message('Password Reset Request', sender='harryyoung542@gmail.com', recipients=[user.email], body=body)

  mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for("dashboard"))

  form = ResetForm(request.form)

  if form.validate():
    user = Users.query.filter_by(email = form.email.data).first()
    send_reset_email(user)
    flash('An email has been sent to reset your password!', 'info')
    return redirect(url_for('login'))


  return render_template("reset_request.html", form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated:
    return redirect(url_for("dashboard"))

  user = Users.verify_reset_token(token)
  if user is None:
    flash('Invalid or Expired Token', 'warning')
    return redirect(url_for('reset_request'))

  form = ResetPasswordForm(request.form)
  if request.method == 'POST' and form.validate():
    h_password = generate_password_hash(
        form.password.data, method='pbkdf2:sha256', salt_length=8)

    user.hash = h_password
    db.session.commit()
    flash('You password is reset.', 'success')
    return redirect(url_for("login"))
  return render_template("reset_token.html", form=form)
