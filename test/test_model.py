import pytest
from sqlalchemy import create_engine
import db
from db import Session
from model import model
from model.model import *
import datetime

@pytest.yield_fixture(scope="module")
def connection():
    # in-memory sqlite database
    engine = create_engine('sqlite://')

    # Create tables
    model.Base.metadata.create_all(engine)

    # Establish connection, reconfigure session to use the test db
    connection = engine.connect()
    db.Session.configure(bind = connection)
    model.Base.metadata.bind = engine

    yield connection

    # Teardown
    model.Base.metadata.drop_all()


@pytest.yield_fixture
def db_session(connection):
    transaction = connection.begin()

    yield Session()

    # Teardown
    transaction.rollback()


class TestWorkHours:

    #test if the db relations are generated correctly
    def test_user_workhours_relation_db(self, db_session):
        user1, user2 = User('user_1'), User('user_2')
        db_session.add(user1)
        db_session.add(user2)
        d = datetime.date.today()
        currentMonth = d.month
        workinghours1_1 = WorkedHours('user_1', currentMonth, 1, 12, 'programming')
        workinghours1_2 = WorkedHours('user_1', currentMonth, 2, 8, 'fact checking')
        workinghours2_1 = WorkedHours('user_2', currentMonth, 3, 4, 'fact checking')
        db_session.add(workinghours1_1)
        db_session.add(workinghours1_2)
        db_session.add(workinghours2_1)

        #testing insertion
        assert db_session.query(User).count() == 2
        assert db_session.query(WorkedHours).count() == 3

        #testing relation one-to-many works
        db_session.delete(user1)
        assert db_session.query(User).count() == 1
        assert db_session.query(WorkedHours).count() == 1


def test_db_sanity_check_rollback(db_session):
    assert db_session.query(WorkedHours).count() == 0