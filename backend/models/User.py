from sqlalchemy import Column, Integer, String, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os, binascii
from database.Base import Base

def verify_email_send(email):
    # send verify email
    return

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), index=True, nullable=False, unique=False)
    email = Column(String(255), unique=True)
    password = Column(String(400), unique=False, nullable=True)
    emailToken = Column(String(40), unique=True)
    disabled = Column(BOOLEAN, unique=False, default=False)
    verified = Column(BOOLEAN, unique=False, default=False)
    profile_pic  = Column(String(300), unique=True, nullable=True)
    admin = Column(BOOLEAN, unique=False, default=False)
    developer = Column(BOOLEAN, unique=False, default=False)
    twitter = relationship("Twitter", backref="user", lazy='selectin')
    google = relationship("Google", backref="user", lazy='selectin')
    discord = relationship("Discord", backref="user", lazy='selectin')

    def __init__(self, username, email, disabled, password=None):
        self.username = username
        self.email = email
        self.disabled = disabled
        self.password = password
        self.emailToken = binascii.hexlify(os.urandom(20)).decode()
