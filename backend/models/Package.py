from sqlalchemy import Column, Integer, String, BOOLEAN, Date, cast, DECIMAL
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from database.MutableList import MutableList
import datetime

Base = declarative_base()


def get_total_downloads(db, package, days_back):
    if downloads := db.get_downloads(package):
        return len([download for download in
                    [datetime.datetime.strptime(download_date, '%Y-%m-%d').date() for download_date in downloads] if (
                                datetime.datetime.now() - datetime.timedelta(
                            days=days_back)).date() <= download <= datetime.date.today()])
    print('return here')
    return 0


class Package(Base):
    __tablename__ = 'packages'
    id = Column(Integer, primary_key=True, nullable=False)
    packageid = Column(String(255), index=True, nullable=False, unique=True)
    developer = Column(String(255), nullable=False, unique=False)
    downloads = Column(MutableList.as_mutable(ARRAY(String)), unique=False)
    price = Column(DECIMAL(18, 2), nullable=False)

    def __init__(self, packageid, developer, price):
        self.packageid = packageid
        self.developer = developer
        self.downloads = []
        self.price = price
