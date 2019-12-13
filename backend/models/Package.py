from sqlalchemy import Column, Integer, String, BOOLEAN, Date, cast, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from database.MutableList import MutableList
import datetime
from database.Base import Base


def get_total_downloads(db, package, days_back):
    if downloads := db.get_downloads(package):
        return len([download for download in [datetime.datetime.strptime(download_date, '%Y-%m-%d').date() for download_date in downloads] if (datetime.datetime.now() - datetime.timedelta(days=days_back)).date() <= download <= datetime.date.today()])
    return 0


class Package(Base):
    __tablename__ = 'package'
    id = Column(Integer, primary_key=True, nullable=False)
    packageid = Column(String(255), index=True, nullable=False, unique=True)
    developer_id = Column(Integer, ForeignKey('user.id'))
    downloads = Column(MutableList.as_mutable(ARRAY(String)), unique=False)
    price = Column(DECIMAL(18, 2), nullable=False)
    purchases = relationship("Purchase", backref="package", lazy='selectin')

    def __init__(self, packageid, developer_id, price):
        self.packageid = packageid
        self.developer_id = developer_id
        self.downloads = []
        self.price = price
