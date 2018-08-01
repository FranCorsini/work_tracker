import db
import sys
import signal
from view.view import MainView
from controller.controller import MainController


class WorkTracker():
    def __init__(self, sys_argv):
        super(WorkTracker, self).__init__()

        self.mainController = MainController()
        self.mainView = MainView(self.mainController)


if __name__ == '__main__':
    # Enable ctrl-c closeable
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    db.initialize()

    app = WorkTracker(sys.argv)




