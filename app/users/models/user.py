from app.database import db
from app import bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(128), unique=False)
    email = db.Column(db.String(), unique=False)

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

