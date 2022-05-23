from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, default = datetime.utcnow)
    isadmin = db.Column(db.Boolean, default = False)

    def __repr__(self):
        return "User " + str(self.id)

class Avatar(db.Model):
    __bind_key__ = "avatars"
    id = db.Column(db.Integer, primary_key=True)
    img_link = db.Column(db.String(100), nullable=False)
    img_username = db.Column(db.String(100), nullable=False, unique=True)
    datetime = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return "Avatar " + str(self.id)

class MusicSheet(db.Model):
    __bind_key__ = "music_sheets"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100))
    datetime = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return "Music Sheet " + str(self.id)

class Comment(db.Model):
    __bind_key__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Comment " + str(self.id)

class Message(db.Model):
    __bind_key__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Message " + str(self.id)

class LearnTeach(db.Model):
    __bind_key__ = "learn_teach_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    is_searching = db.Column(db.String(100))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Learn/Teach " + str(self.id)

class Book(db.Model):
    __bind_key__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(70))
    rating = db.Column(db.Integer)
    img = db.Column(db.String)
    review = db.Column(db.String)

    @staticmethod
    def insert_one(data):
        Book1 = Book(name = data["name"], author = data["author"], rating = data["rating"], img = data["img"], review = data["review"])
        db.session.add(Book1)
        db.session.commit()

    @staticmethod
    def find_all():
        search_matches = [{"name":vars(item)["name"], "author":vars(item)["author"], "rating":vars(item)["rating"], "img":vars(item)["img"], "review":vars(item)["review"]} for item in Book.query.all()]
        return search_matches

    @staticmethod
    def delete_all():
        db.session.query(Book).delete()
        db.session.commit()

    @staticmethod
    def delete_one(data):
        Book.query.filter_by(name = data["name"]).delete()
        db.session.commit()

    def __repr__(self):
        return "Book " + str(self.id)