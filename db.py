from model.model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import os
import re

Session = scoped_session(sessionmaker())


def initialize():
    basepath = os.path.dirname(__file__)
    connection_string = os.path.abspath(os.path.join(basepath, os.pardir, "work_tracker/data/db.sqlite"))

    #workaround to create folder if it doesn't exist (otherwise throws error, it doesn't generate it)
    connection_string = 'sqlite:///' + connection_string
    if connection_string.startswith('sqlite'):
        db_file = re.sub("sqlite.*:///", "", connection_string)
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
    engine = create_engine(connection_string)

    Base.metadata.create_all(engine)

    Session.configure(bind=engine)


@contextmanager
def sessionScope():

    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
