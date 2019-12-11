from sqlalchemy import Column, Integer, String, BOOLEAN, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import os, binascii
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), index=True, nullable=False, unique=False)
    email = Column(String(255), unique=True)
    emailToken = Column(String(40), unique=True)
    disabled = Column(BOOLEAN, unique=False, default=False)
    verified = Column(BOOLEAN, unique=False, default=False)
    password = Column(String(400), unique=False)

    def __init__(self, username, email, disabled, password):
        self.username = username
        self.email = email
        self.disabled = disabled
        self.password = password
        self.emailToken = binascii.hexlify(os.urandom(20)).decode()


class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(String(100), nullable=False)
    processor = Column(String(100), nullable=False)
    package = Column(String(255), index=True, nullable=False)
    price = Column(DECIMAL(18, 2), nullable=False)
    discount = Column(DECIMAL(18, 2), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

    def __init__(self, user, processor, package, price, discount=0):
        self.purchaser_id = user
        self.date = datetime.datetime.today().date()
        self.processor = processor
        self.package = package
        self.price = price
        self.discount = discount
