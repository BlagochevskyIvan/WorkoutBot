from db.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=True)
    payments = relationship("Payment", back_populates="user")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    telegram_id = Column(BigInteger, index=True)
    status = Column(String, default='Pending')
    amount = Column(Integer, nullable=False)
    user = relationship("User", back_populates="payments")