from os import getenv

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tid = Column(Integer, nullable=False)  # bigint заменен на Integer
    name = Column(String(255))  # tinytext
    faculty = Column(Integer, nullable=False)
    group = Column(Integer, nullable=False)

    marked_schedules = relationship("MarkedSchedule", back_populates="user")


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # tinytext
    caption = Column(String(300), nullable=False)  # tinytext
    yandex_maps_id = Column(String(300), nullable=False)  # tinytext


class MarkedSchedule(Base):
    __tablename__ = 'marked_schedule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)  # tinytext
    href = Column(String(255), nullable=False)  # tinytext
    type = Column(String(255), nullable=False)  # tinytext

    user = relationship("User", back_populates="marked_schedules")


class Notifications(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tid = Column(Integer, ForeignKey('users.id'), nullable=False)
    schedule_corrections = Column(String(1), nullable=False, default='1')  # tinytext
    schedule_notify = Column(String(1), nullable=False, default='1')  # tinytext
    service_msgs = Column(String(1), nullable=False, default='1')  # tinytext


class Database:
    def __init__(self):
        self.session = None

    def db_reconnect(self):
        try:
            self.session.close()
        except Exception as e:
            pass
        engine = create_engine(
            f'mysql+pymysql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}'
            f'@{getenv('DB_HOST')}/{getenv('DB_NAME')}')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_user_by_tid(self, tid: int) -> User:
        self.db_reconnect()
        return self.session.query(User).filter_by(tid=tid).first()

    def create_new_user(self, tid: int, faculty: int, group: int):
        self.db_reconnect()
        self.session.add(User(tid=tid, faculty=faculty, group=group))
        self.session.add(Notifications(tid=tid))
        self.session.commit()

    def get_place_info(self, place_name) -> Location:
        self.db_reconnect()
        return self.session.query(Location).filter_by(name=place_name).first()

    def get_user_notifications_statuses(self, tid: int) -> Notifications:
        self.db_reconnect()
        return self.session.query(Notifications).filter_by(tid=tid).first()

    def update_user_notification_statuses(self, tid: int, schedule_update, lesson_reminder, service_message):
        data = {
            'schedule_corrections': schedule_update,
            'schedule_notify': lesson_reminder,
            'service_msgs': service_message,
        }
        self.db_reconnect()
        self.session.query(Notifications).filter_by(tid=tid).update(data)
        self.session.commit()

    def edit_user_name(self, tid: int, name: str):
        data = {
            'name': name
        }
        self.db_reconnect()
        self.session.query(User).filter_by(tid=tid).update(data)
        self.session.commit()
