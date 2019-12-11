from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.orm import sessionmaker
from models.User import User, Purchase, Base
from models.Package import Package, Base
import datetime


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

    def insert_package(self, package: str = None, price: float = 0.00):
        self.session.add(Package(package, "supremevance123", price))
        self.session.commit()

    def add_download(self, package: str = None):
        if downloads := self.session.query(Package).filter(Package.packageid == package).all():
            if len(downloads) > 0:
                downloads[0].downloads.append(datetime.date.today())
                self.session.commit()
                return

    def get_downloads(self, package):
        if downloads := self.session.query(Package).filter(Package.packageid == package).all():
            if len(downloads) > 0:
                return downloads[0].downloads

    def add_purchase(self, user, processor, package, price, discount):
        if len(self.session.query(Purchase).filter(Purchase.purchaser_id == user.id and Purchase.package == package).all()) <= 0:
            self.session.add(Purchase(user["id"], processor, package, price, discount))
            return True
        return False

    def is_package(self, package):
        if len(self.session.query(Package).filter(Package.packageid == package).all()) > 0:
            return True
        return False

    def info_package(self, package):
        if package := self.session.query(Package).filter(Package.packageid == package).all()[0]:
            return package
        return
