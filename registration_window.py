from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from dashboard import DashBoard

class RegistrationWindow(QMainWindow):
    def __init__(self):
        super(RegistrationWindow, self).__init__()
        loadUi('ui/registration.ui',self)

        self.dashboard = DashBoard()
        self.register_button.clicked.connect(self.go_to_register)
        self.show()
    def go_to_register(self):
        print("go to the register page")
        self.close()
        if self.dashboard.isVisible():
            print("Dashboard is Openned!")
        else:
            self.dashboard.create_g_dash()
            self.dashboard.show()
    # def go_to_dashboard(self):
        
            #self.dashboard.start_detection()