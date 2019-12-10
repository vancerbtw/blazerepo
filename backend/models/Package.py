from sqlalchemy import Column, Integer, String, BOOLEAN, Date, cast
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from database.MutableList import MutableList
import numpy as np
import datetime

Base = declarative_base()


def get_total_downloads(db, package, days_back):
    downloads = np.array([datetime.datetime.strptime(download_date, '%Y-%m-%d').date() for download_date in
                          db.get_downloads(package)])
    return len(np.where((downloads <= datetime.date.today()) & (
                downloads >= (datetime.datetime.now() - datetime.timedelta(days=days_back)).date()))[0])


class Package(Base):
    __tablename__ = 'packages'
    id = Column(Integer, primary_key=True, nullable=False)
    packageid = Column(String(255), index=True, nullable=False, unique=True)
    developer = Column(String(255), nullable=False, unique=False)
    downloads = Column(MutableList.as_mutable(ARRAY(String)), unique=False)

    def __init__(self, packageid, developer):
        self.packageid = packageid
        self.developer = developer
        self.downloads = []
