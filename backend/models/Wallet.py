from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database.Base import Base


class Wallet(Base):
    __tablename__ = 'wallet'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    amount = Column(DECIMAL(18, 2), nullable=False, default=0.00)
    deposits = relationship("Deposit", backref="wallet", lazy='selectin', uselist=True)

    def __init__(self, user_id):
        self.user_id = user_id
        self.amount = 0.00
