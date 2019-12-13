from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from database.Base import Base

class Purchase(Base):
    __tablename__ = 'purchase'
    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(String(100), nullable=False)
    processor = Column(String(100), nullable=False)
    package_id = Column(Integer, ForeignKey('package.id'))
    price = Column(DECIMAL(18, 2), nullable=False)
    discount = Column(DECIMAL(18, 2), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, user, processor, package, price, discount=0):
        self.user_id = user.id
        self.date = datetime.datetime.today().date()
        self.processor = processor
        self.package = package
        self.price = price
        self.discount = discount