from sqlalchemy import Column, Integer, String, BOOLEAN
from sqlalchemy.orm import relationship
from database.Base import Base
import uuid

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), index=True, nullable=False, unique=False)
    email = Column(String(255), unique=True)
    password = Column(String(400), unique=False, nullable=True)
    emailToken = Column(String(36), unique=True, default=uuid.uuid4().hex)
    disabled = Column(BOOLEAN, unique=False, default=False)
    verified = Column(BOOLEAN, unique=False, default=False)
    profile_pic  = Column(String(300), unique=True, nullable=True)
    admin = Column(BOOLEAN, unique=False, default=False)
    developer = Column(BOOLEAN, unique=False, default=False)
    twitter = relationship("Twitter", backref="user", lazy='selectin', uselist=False)
    google = relationship("Google", backref="user", lazy='selectin', uselist=False)
    discord = relationship("Discord", backref="user", lazy='selectin', uselist=False)
    purchases = relationship("Purchase", backref="user", lazy='selectin', uselist=True)
    packages = relationship("Package", backref="user", lazy='selectin', uselist=True)
    wallet = relationship("Wallet", backref="user", lazy='selectin', uselist=False)

    def __init__(self, username, email, disabled, password=None):
        self.username = username
        self.email = email
        self.disabled = disabled
        self.password = password
