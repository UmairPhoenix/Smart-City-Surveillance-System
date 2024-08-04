from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
from v_dash import V_Dash
from bag_window import BagWindow
class VehicleWindow(QMainWindow):
    def __init__(self):
        super(VehicleWindow, self).__init__()
        self.v_dash = V_Dash()
        loadUi('ui/vehicle.ui',self)
        self.start_button.clicked.connect(self.start_counting)
        self.stop_button.clicked.connect(self.stop_counting)
        self.signout_button.clicked.connect(self.sign_out)
        self.luggage_button.clicked.connect(self.luggage_monitoring)
        self.import_button.clicked.connect(self.importVideo)
    def create_v_dash(self):
        self.v_dash=V_Dash()
        self.show()
    @pyqtSlot(QImage)
    def setImage(self,image):
        self.v_window.setPixmap(QPixmap.fromImage(image))
    
    def start_counting(self):
        self.v_dash.running = True
        self.v_dash.changePixmap.connect(self.setImage)
        self.v_dash.start()
        self.show()
    def stop_counting(self):
        
        self.v_dash.running = False
        print('Counting is Stopped')
    def sign_out(self):
        self.close()
    def luggage_monitoring(self):
        self.b_window=BagWindow()
        self.b_window.displayInfo()
        self.close()
    def importVideo(self):
        video_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4 *.avi)")
        if video_path:
            self.v_dash.setVideoPath(video_path)
    def displayInfo(self):
        self.show()