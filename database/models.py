from sqlalchemy import Column, Integer, BigInteger, DateTime, String, VARCHAR, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    telegram_id = Column(BigInteger, nullable=False)
    faculty = Column(Integer, nullable=False)
    group = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    caption = Column(VARCHAR(300), nullable=False, default="Описание отсутствует")
    maps_id = Column(VARCHAR(100), nullable=False)

class UserSchedule(Base):
    __tablename__ = 'marked_schedule'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    href = Column(VARCHAR(300), nullable=False)
    type = Column(VARCHAR(100), nullable=False)
