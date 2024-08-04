from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from p_dash import P_Dash
from PyQt5.QtWidgets import QFileDialog
from vehicle_window import VehicleWindow
from bag_window import BagWindow
class ParkingWindow(QMainWindow):
    def __init__(self):
        super(ParkingWindow, self).__init__()
        self.p_dash = P_Dash()
        loadUi('ui/parking.ui',self)
        self.detect_button.clicked.connect(self.count_space)
        self.signout_button.clicked.connect(self.sign_out)
        self.stop_detection_button.clicked.connect(self.stop_detection)
        self.vehicle_button.clicked.connect(self.open_vehicle_monitoring)
        self.luggage_button.clicked.connect(self.luggage_monitoring)
        self.import_button.clicked.connect(self.importVideo)
        #self.set_cam.clicked.connect(self.setCamera)
    def create_p_dash(self):
        self.p_dash=P_Dash()
        self.show()
    @pyqtSlot(QImage)
    def setImage(self,image):
        self.p_window.setPixmap(QPixmap.fromImage(image))
    def open_vehicle_monitoring(self):
        self.vehicle_window=VehicleWindow()
        self.vehicle_window.displayInfo()
        self.close()
    def count_space(self):
        self.p_dash.changePixmap.connect(self.setImage)
        self.p_dash.start()
        self.show()
    def sign_out(self):
        self.close()
    def stop_detection(self):
        self.p_dash.running = False
    def luggage_monitoring(self):
        self.b_window=BagWindow()
        self.b_window.displayInfo()
        self.close()
    def importVideo(self):
        video_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4 *.avi)")
        if video_path:
            self.p_dash.setVideoPath(video_path)
    # def setCamera(self):
    #     self.p_dash.setVideoPath(0)
    def displayInfo(self):
        self.show()