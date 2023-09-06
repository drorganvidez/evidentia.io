from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

from app import db


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), nullable=False)
    updated_at = db.Column(DateTime, default=datetime.utcnow)

    avatar_id = db.Column(db.Integer, db.ForeignKey('avatar.id'), nullable=True)
    avatar = relationship('Avatar', back_populates='user_profile')

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()


class Avatar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)

    from app.file.models import File
    file = relationship('File')

    user_profile = relationship('UserProfile', back_populates='avatar')
