from . import db 
from flask_login import UserMixin
# from sqlalchemy.sql import func 
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)

class Post(db.Model):
    blogid = db.Column(db.Integer, primary_key=True)
    blogtitle = db.Column(db.String(400), nullable=False)
    blogdesc = db.Column(db.Text, nullable=False)
    blogtype = db.Column(db.String(50), nullable=False)
    blogimage = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.Integer,db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

class Comment(db.Model):
    commentid = db.Column(db.Integer, primary_key=True)
    commentdesc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.Integer,db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.blogid', ondelete='CASCADE'), nullable=False)

class Like(db.Model):
    likeid = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.Integer,db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.blogid', ondelete='CASCADE'), nullable=False)