from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database.Base import Base

class Deposit(Base):
    __tablename__ = 'deposit'
    id = Column(Integer, primary_key=True, nullable=False)
    wallet_id = Column(Integer, ForeignKey('wallet.id'))
    amount = Column(DECIMAL(18, 2), nullable=False)

    def __init__(self, wallet_id, amount):
        self.wallet_id = user_id
        self.amount = amount
