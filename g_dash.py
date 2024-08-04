from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import cv2
import time
import torch
from PyQt5.QtWidgets import QMessageBox  # Import for dialog box (used in the main thread)

class G_Dash(QThread):
    changePixmap = pyqtSignal(QImage)
    showDialog = pyqtSignal(str)  # Signal to show dialog box
    running = True

    def __init__(self):
        super(G_Dash, self).__init__()
        self.detection_start_time = None  # Initialize the start time for detection
        self.detection_time_threshold = 5  # Time in seconds to trigger the screenshot
    def setVideoPath(self, path):
        self.video_path = path
    def run(self):
        classNames = ['knife', 'pistol']
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='./weights/weapon.pt')
        self.running = True
        #cap = cv2.VideoCapture('./video/weapon_1.mp4')
        #   # Starts camera
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if ret:
                # Make detection
                results = model(frame)
                results.render()  # Draw bounding boxes on the frame
                weapon_detected = False

                # Check if any weapons were detected with confidence > 0.5
                for *_, conf, cls in results.xyxy[0]:
                    if conf > 0.5 and classNames[int(cls)] in classNames:
                        weapon_detected = True
                        if self.detection_start_time is None:
                            self.detection_start_time = time.time()  # Start the timer
                        break

                # If weapon is detected and the time threshold is passed, save the screenshot and emit the signal
                if weapon_detected and (time.time() - self.detection_start_time) > self.detection_time_threshold:
                    timestamp = self.save_detection(frame)
                    self.showDialog.emit(f"Weapon is detected. Please check the timestamped screenshot: {timestamp}")
                    self.detection_start_time = None  # Reset the timer after taking a screenshot
                elif not weapon_detected:
                    self.detection_start_time = None  # Reset the timer if no weapon is detected

                # Convert frame to QImage and emit the changePixmap signal
                height, width, channels = frame.shape
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                bytesPerLine = channels * width
                convertToQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(676, 512, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

        cap.release()  # Release the video capture object
        cv2.destroyAllWindows()

    def save_detection(self, frame):
        timestamp = time.strftime("%Y%m%d-%H%M%S")  # Get current time for a unique filename
        cv_path = f"screenshots/gun_det_{timestamp}.jpg"
        cv2.imwrite(cv_path, frame)
        print("Screenshot Saved")
        return timestamp  # Return the timestamp for the dialog box
