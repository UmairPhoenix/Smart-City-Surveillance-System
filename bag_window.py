import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from b_dash import B_Dash
from PyQt5.QtWidgets import QFileDialog
class BagWindow(QMainWindow):
    def __init__(self):
        super(BagWindow, self).__init__()
        self.b_dash = B_Dash()
        loadUi('ui/luggage.ui',self)
        self.start_button.clicked.connect(self.suitcase_monitoring)
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.signout_button.clicked.connect(self.sign_out)
        self.view_ss_button.clicked.connect(self.open_ss)
        self.import_button.clicked.connect(self.importVideo)
    def create_b_dash(self):
        self.b_dash=B_Dash()
        self.show()
    @pyqtSlot(QImage)
    def setImage(self,image):
        self.b_window.setPixmap(QPixmap.fromImage(image))
    
    def suitcase_monitoring(self):
        self.b_dash.running = True
        self.b_dash.changePixmap.connect(self.setImage)
        self.b_dash.start()
        self.show()
    def stop_monitoring(self):
        
        self.b_dash.running = False
        print('Monitoring is Stopped')
    def sign_out(self):
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
            self.b_dash.setVideoPath(video_path)
    def displayInfo(self):
        self.show()