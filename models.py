from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    can_modify = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Data:\nID: {self.id}\nUser: {self.user}\nPassword: -\nCan Modify: {self.can_modify}\n Admin: {self.is_admin}\n'
