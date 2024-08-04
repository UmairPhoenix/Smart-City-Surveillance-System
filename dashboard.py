import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from g_dash import G_Dash
from parking_window import ParkingWindow
from vehicle_window import VehicleWindow
from bag_window import BagWindow
from PyQt5.QtWidgets import QFileDialog
class DashBoard(QMainWindow):
    def __init__(self):
        super(DashBoard, self).__init__()
        loadUi('ui/dashboard.ui',self)
        
        self.detect_button.clicked.connect(self.start_detection)
        self.stop_detection_button.clicked.connect(self.stop_detection)
        self.park_button.clicked.connect(self.go_to_parking)
        self.signout_button.clicked.connect(self.sign_out)
        self.view_ss_button.clicked.connect(self.open_ss)
        self.vehicle_button.clicked.connect(self.open_vehicle_monitoring)
        self.luggage_button.clicked.connect(self.luggage_monitoring)
        self.import_button.clicked.connect(self.importVideo)
    def create_g_dash(self):
        self.g_dash=G_Dash()
        self.g_dash.changePixmap.connect(self.setImage)
        self.g_dash.showDialog.connect(self.show_warning_dialog)
        self.show()
    @pyqtSlot(QImage)
    def setImage(self,image):
        self.g_window.setPixmap(QPixmap.fromImage(image))
    
    @pyqtSlot(str)
    def show_warning_dialog(self, message):
        QMessageBox.warning(self, "Warning", message)


    def start_detection(self):
        
        self.g_dash.changePixmap.connect(self.setImage)
        
        self.g_dash.start()
        self.show()

    def stop_detection(self):
        self.g_dash.running = False
        
    # def displayInfo(self):
    #     self.show()
    
    def go_to_parking(self):
        self.parking_window=ParkingWindow()
        self.parking_window.displayInfo()
        self.close()
    def sign_out(self):
        self.close()
    def open_vehicle_monitoring(self):
        self.vehicle_window=VehicleWindow()
        self.vehicle_window.displayInfo()
        self.close()
    def luggage_monitoring(self):
        self.b_window=BagWindow()
        self.b_window.displayInfo()
        self.close()
    

    def open_ss(self):
        folder_path = os.path.abspath('./screenshots')

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            os.system(f'explorer "{folder_path}"')  # Open the folder using the default file explorer
        else:
            print("The 'screen_shots' folder does not exist.")
    def importVideo(self):
        video_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4 *.avi)")
        if video_path:
            self.g_dash.setVideoPath(video_path)