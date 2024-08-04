from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from dashboard import DashBoard
from registration_window import RegistrationWindow
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi('ui/login_window.ui',self)
        
        self.dashboard = DashBoard()
        self.register_button.clicked.connect(self.go_to_register)
        self.login_button.clicked.connect(self.go_to_dashboard)
        self.show()
        

    def go_to_register(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()
        self.close()
        self.registration_window.show()
        print("go to the register page")
    
    def go_to_dashboard(self):
        self.close()
        
        if self.dashboard.isVisible():
            print("Dashboard is Openned!")
        else:
            self.dashboard.create_g_dash()
            self.dashboard.show()
            #self.dashboard.start_detection()