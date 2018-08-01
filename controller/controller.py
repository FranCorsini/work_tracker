
import logging

from sqlalchemy import func

from model.model import User, WorkedHours
import datetime
import pandas as pd

class MainController(object):

    # create logger with 'spam_application'
    global logger
    logger = logging.getLogger('worktracker')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('controller.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info('Lets start')
    logger.info('Just created Controller')

    #returns the hours the current user worked this month
    def calculateHoursInCurrentMonth(self, user, session):
        d = datetime.date.today()
        month = d.month

        for row in session.query(WorkedHours).filter(WorkedHours.name == str(user)):
            print(str(row))

        total = 0
        for hours in session.query(WorkedHours.hours).\
                filter(WorkedHours.name == str(user),WorkedHours.month == month):
            total = total + hours.hours
        return total


    def addHours(self, user, day, hours, topic, session):
        d = datetime.date.today()
        month = d.month
        workedHours = WorkedHours(str(user),month,day,hours,topic)
        session.add(workedHours)

    # it returns the table with all the Topics worked by users and the amount of hours
    def generateReport(self, session):

        #I write the SQL to manage to write the python query
        '''
        SELECT topic, sum(hours)
        FROM WorkedHours
        GROUP BY topic
        ORDER BY hours
        '''
        d = []
        for elem in session.query(
                WorkedHours.topic,
                func.sum(WorkedHours.hours)
            ). \
                group_by(WorkedHours.topic). \
                order_by(func.sum(WorkedHours.hours).desc()). \
                all():
            #fill the data
            d.append((elem[0], elem[1]))
        #create the pandas dataframe
        df = pd.DataFrame(d)
        return df


    def getObject(self, obj, id, session):
        "Generic get object"
        return session.query(obj).get(id)

    def getObjects(self, obj, session):
        "Generic get all objects"
        return session.query(obj).all()

    def newUser(self, userLabel, session):
        user = User(userLabel)
        session.add(user)
        return self.getObject(User, userLabel, session)

    def loadUser(self, name, session):
        return self.getObject(User, name, session)

    def loadUsers(self, session):
        return self.getObjects(User,session)



