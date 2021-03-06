from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from passbank import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  hash = db.Column(db.String(100), unique=True, nullable=False)
  passwords = db.relationship('Password', backref='owner', lazy=True)

  def get_reset_token(self, expires_sec=1800):
    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': self.id}).decode('utf-8')

  @staticmethod
  def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
      user_id = s.loads(token)['user_id']
    except:
      return None
    return Users.query.get(user_id)

  def __repr__(self):
    return f"Users('{self.username}', '{self.email}', '{self.hash}')"


class Password(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  website = db.Column(db.String(200), nullable=False)
  url = db.Column(db.String(200), nullable=False)
  username = db.Column(db.String(100), nullable=False)
  password = db.Column(db.String(100), nullable=False)
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  def __repr__(self):
    return f"Password('{self.website}', '{self.username}'"
