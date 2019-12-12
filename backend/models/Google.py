from sqlalchemy import Column, Integer, String, BOOLEAN, DECIMAL, ForeignKey
from database.Base import Base

class Google(Base):
    __tablename__ = 'google'
    id = Column(Integer, primary_key=True, nullable=False)
    google_id = Column(String(80), nullable=False)
    email = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    picture = Column(String(300), unique=True, nullable=True)

    def __init__(self, google_user, user_id):
        self.google_id = google_user['id']
        self.email = google_user['email']
        self.name = google_user['name']
        self.user_id = user_id
        self.picture = google_user['picture']
