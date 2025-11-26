from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from db import db




class Jobs(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    long_description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    company = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Job {self.title}>'


class Job(db.Model):
     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     title = db.Column(db.String(100), nullable=False)
     short_description = db.Column(db.Text, nullable=False)
     long_description = db.Column(db.Text, nullable=False)
     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
     company = db.Column(db.String(100), nullable=False)
     author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

     def __repr__(self):
         return f'<Job {self.title}>'



class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), unique=True,  nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)
    jobs = db.relationship('Job', backref='author',)
    image = db.Column(db.String(200), nullable=True, default='default.jpg')


    def __repr__(self):
        return f"User ( '{self.username}' , '{self.email}', '{self.image}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    @property
    def password(self):
        raise AttributeError('პაროლს ვერ წაიკითხავ')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)






