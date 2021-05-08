# Import packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import backref


# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a741b74ca4cb521cf4bbf3f3cfdbd5c5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passbank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from passbank import routes
