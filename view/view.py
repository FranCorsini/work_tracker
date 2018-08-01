import logging
from db import sessionScope
import time

# not really a view but whatever, to keep the MVC alive

class MainView():
    def __init__(self, mainController):
        self.mc = mainController
        self.currentUser = None

        self.setupLogs()

        #open the db connection
        with sessionScope() as session:
            self.logIn(session)
            input_command = None

            #listen for commands until exit
            while input_command != "exit":
                self.interactiveShell()
                input_command = input("Type command: ")

                #I know there are much better ways than doing this horrible if/else monster, please forgive me
                if input_command == "show":
                    for elem in self.mc.loadUsers(session):
                        print(str(elem))
                elif input_command == "ins":
                    self.addWorkingHours(session)
                elif input_command == "hours":
                    self.showHours(session)
                elif input_command == "report":
                    self.printReport(session)
                elif input_command == "help":
                    self.help()


            print("bye bye")

    #main view
    def interactiveShell(self):
        time.sleep(1)
        print("type help for list of commands")


    def help(self):
        print("here is the list of commands:")
        print("\"show\": show list of users")
        print("\"ins\": insert hours for this month")
        print("\"hours\": show hours you worked this month")
        print("\"report\": generates report of tasks worked by everyone ")
        print("\"exit\": bye ")

    def printReport(self, session):
        table = self.mc.generateReport(session)
        table.columns = ['topic', 'hours']
        print(table)


    def showHours(self,session):
        ret = self.mc.calculateHoursInCurrentMonth(self.currentUser,session)
        print("You have worked " + str(ret) + " hours this month")

    def addWorkingHours(self,session):
        day = input("Which day you want to add hours to?(int): ")
        hours = input("How many hours? ")
        topic = input("What have you been working on? ")
        self.mc.addHours(self.currentUser, day, hours, topic, session)
        print("Hours added")

    #well this is just the basic, just with a username
    def logIn(self,session):
        # ask for "logging in"
        input_var = input("Enter username: ")

        # try to retrieve user information or create a new one
        user = self.mc.loadUser(input_var, session)
        if (user == None):
            print("username not found")
            print("creating new username " + input_var)
            self.mc.newUser(input_var,session)
            user = self.mc.loadUser(input_var, session)
            print("user created")
        else:
            print("Welcome back user " + str(user) + ",\n")
        # save User for current session
        self.currentUser = user


    def setupLogs(self):
        # create logger with 'spam_application'
        global logger
        logger = logging.getLogger('worktracker')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('View.log')
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
        logger.info('Just created Main view')


