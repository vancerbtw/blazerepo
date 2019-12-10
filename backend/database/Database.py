from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.orm import sessionmaker
from models.User import User, Base


class Database:
    def __init__(self, connection_string):
        self.db = create_engine(connection_string)
        Session = sessionmaker(bind=self.db)
        self.session = Session()
        Base.metadata.create_all(self.db)

    def add_user(self, user: User):
        self.session.add(user)
        self.session.commit()

    def user_exists(self, email: str = None):
        exists = self.session.query(
            self.session.query(User).filter_by(email=email).exists()
        ).scalar()
        return exists

    def get_user(self, email: str = None):
        if user := self.session.query(User).filter(User.email == email).all():
            print(user)
            return user[0]
        return
