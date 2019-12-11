from sqlalchemy import Column, Integer, String, BOOLEAN, DECIMAL, ForeignKey
from database.Base import Base

class Twitter(Base):
    __tablename__ = 'twitter'
    id = Column(Integer, primary_key=True, nullable=False)
    twitter_id = Column(String(80), nullable=False)
    email = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, twitter_id, email, name, user_id):
        self.twitter_id = twitter_id
        self.email = email
        self.name = name
        self.user_id = user_id
