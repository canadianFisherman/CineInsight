from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, app

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    reviews = db.relationship('Review', back_populates='movie')
    genre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'{self.title}'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', ondelete="CASCADE"))
    movie = db.relationship('Movie', back_populates='reviews')

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_review_user'), nullable=False)
    # user = db.relationship('User', back_populates='reviews')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # reviews = db.relationship('Review', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
