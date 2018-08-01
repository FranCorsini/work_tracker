import pytest
from sqlalchemy import create_engine
import db
from db import Session
from model import model
from model.model import *
from controller.controller import MainController

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

    #test the controller logic for creation of objs
    def test_user_workhours_creation_logic(self, db_session):
        self.mc = MainController()

        self.mc.newUser('user1', db_session)
        self.mc.newUser('user2', db_session)

        self.mc.addHours('user_1', 1, 12, 'programming', db_session)
        self.mc.addHours('user_1', 2, 8, 'fact checking', db_session)
        self.mc.addHours('user_2', 3, 4, 'fact checking', db_session)

        #testing insertion
        assert db_session.query(User).count() == 2
        assert db_session.query(WorkedHours).count() == 3


    #test if the logic for the hours function is correct
    def test_workhours_count_hours_logic(self, db_session):
        self.mc = MainController()

        user1 = self.mc.newUser('user1', db_session)
        user2 = self.mc.newUser('user2', db_session)

        self.mc.addHours(user1, 1, 12, 'programming', db_session)
        self.mc.addHours(user1, 2, 8, 'fact checking', db_session)
        self.mc.addHours(user2, 3, 4, 'fact checking', db_session)

        #testing function calculateHoursInCurrentMonth
        assert self.mc.calculateHoursInCurrentMonth(user1, db_session) == 20
        assert self.mc.calculateHoursInCurrentMonth(user2, db_session) == 4

