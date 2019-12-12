from sqlalchemy import Column, Integer, String, BOOLEAN, DECIMAL, ForeignKey
from database.Base import Base

class Discord(Base):
    __tablename__ = 'discord'
    id = Column(Integer, primary_key=True, nullable=False)
    discord_id = Column(String(80), nullable=False)
    email = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    picture = Column(String(300), unique=True, nullable=True)

    def __init__(self, discord_user, user_id):
        self.discord_id= discord_user.id
        self.email = discord_user.email
        self.name = discord_user.username
        self.user_id = user_id
        self.picture = discord_user.avatar_url
