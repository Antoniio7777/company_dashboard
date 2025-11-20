from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')

    def __repr__(self):
        return f'Data:\nID: {self.id}\nUser: {self.username}\nPassword: -\nRole: {self.role}\n'
