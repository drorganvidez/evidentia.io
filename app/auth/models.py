from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    profile = db.relationship('UserProfile', backref='user', lazy=True, cascade="all, delete-orphan")

    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    student = db.relationship('Student', backref='user', uselist=False, cascade="all, delete-orphan")
    coordinator = db.relationship('Coordinator', backref='user', uselist=False, cascade="all, delete-orphan")
    secretary = db.relationship('Secretary', backref='user', uselist=False, cascade="all, delete-orphan")
    event_manager = db.relationship('EventManager', backref='user', uselist=False, cascade="all, delete-orphan")
    reviewer = db.relationship('Reviewer', backref='user', uselist=False, cascade="all, delete-orphan")
    lectures = db.relationship('Lecturer', backref='user', uselist=False, cascade="all, delete-orphan")

    def __init__(self, email, password, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.password = generate_password_hash(password)

    @property
    def current_roles(self):
        roles = []

        if self.student:
            roles.append("Student")
        if self.coordinator:
            roles.append("Coordinator")
        if self.secretary:
            roles.append("Secretary")
        if self.event_manager:
            roles.append("EventManager")
        if self.reviewer:
            roles.append("Reviewer")

        return roles

    def get_roles(self):
        return self.roles

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all():
        return User.query.all()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    VALID_ROLES = ['STUDENT', 'COORDINATOR', 'SECRETARY', 'REVIEWER', 'EVENT_MANAGER', 'LECTURER', 'DEVELOPER']

    def __init__(self, name):
        if name not in self.VALID_ROLES:
            raise ValueError(f"The role '{name}' is not valid.")
        self.name = name


user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                      )


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class Coordinator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class Secretary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class EventManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class Reviewer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
