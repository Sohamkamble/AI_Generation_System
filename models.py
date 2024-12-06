from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(50), unique = True, nullable = False, primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)

class Content(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String, db.ForeignKey('users.user_id'), nullable = False)
    prompt = db.Column(db.Text, nullable = False)
    video_paths = db.Column(db.Text, nullable = True)
    image_paths = db.Column(db.Text, nullable = True)
    status = db.Column(db.String(50), default = 'Processing')
    generated_at = db.Column(db.DateTime, default = datetime.now())