from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    name = Column(String, primary_key=True)
    type = Column(String)

    # one-to-many
    workedHours = relationship('WorkedHours',
                               cascade='all, delete-orphan',
                               backref='users')


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class WorkedHours(Base):
    __tablename__ = 'workedhours'

    id = Column(Integer, primary_key=True)
    name = Column(String, ForeignKey('users.name'), nullable=False)
    month = Column(Integer)
    day = Column(Integer)
    hours = Column(Integer)
    topic = Column(String)

    def __init__(self, name, month, day, hours, topic):
        self.name = name
        self.month = month
        self.day = day
        self.hours = hours
        self.topic = topic

    def __repr__(self):
        return "day=%s, hours=%s, topic=%s" % (self.day, self.hours, self.topic)


