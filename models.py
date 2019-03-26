from db import db
from datetime import datetime


class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(50), db.ForeignKey('user.open_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, open_id, name):
        self.open_id = open_id
        self.name = name


class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(50), db.ForeignKey('user.open_id'), nullable=False)
    url = db.Column(db.String(10), nullable=False)
    is_approved = db.Column(db.Boolean(), nullable=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)

    def __init__(self, open_id, url, album_id):
        self.open_id = open_id
        self.url = url
        self.album_id = album_id


class WxUser(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(50))
    name = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(50))
    created = db.Column(db.DATETIME, default=datetime.now())
    last_login = db.Column(db.DATETIME, default=datetime.now())
    user_type = db.Column(db.Integer, default=1)

    def __init__(self, open_id, name, avatar):
        self.open_id = open_id
        self.name = name
        self.avatar = avatar
        self.created = datetime.now()
        self.last_login = datetime.now()
        self.user_type = 1

    def __init__(self, open_id):
        self.open_id = open_id


class Code(db.Model):
    __tablename__ = 'code'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), nullable=False)
    session_key = db.Column(db.String(50))

    def __init__(self, code):
        self.code = code
        self.session_key = ""


class User(db.Model):
    # Columns
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True)
    thrust = db.Column(db.Integer, default=0)

    def __init__(self, name, thrust):
        self.name = name
        self.thrust = thrust

    def __repr__(self):
        return '<User %r>' % self.name

    def __str__(self):
        return '<User %s>' % self.name


class Comment(db.Model):
    # Columns
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True)
    desc = db.Column(db.String(128))

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __repr__(self):
        return '<User %r>' % self.desc

    def __str__(self):
        return '<User %s>' % self.desc
