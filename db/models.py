from db.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    place = Column(String, nullable=True)
    birth_date = Column(String, nullable=True)
    


