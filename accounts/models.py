# models.py
from db_extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(1))
    image_path = db.Column(db.String(255))
    role = db.Column(db.String(20), default='user')  # default role is 'user'

    def __repr__(self):
        return f"<User {self.username} - {self.email} - {self.role}>"


