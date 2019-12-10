from typing import List
from sqlalchemy import Column, Integer, String, BOOLEAN
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, constr
import os, binascii

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