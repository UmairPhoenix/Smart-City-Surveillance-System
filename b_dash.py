from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import cv2
import torch
import time

class B_Dash(QThread):
    changePixmap = pyqtSignal(QImage)
    showDialog = pyqtSignal(str)  # Signal to show dialog box

    def __init__(self):
        super(B_Dash, self).__init__()
        self.running = True
        self.detection_start_time = None  # Initialize the start time for detection
    def setVideoPath(self, path):
        self.video_path = path
    def run(self):
        #cap = cv2.VideoCapture('./image/A.jpg')
        cap = cv2.VideoCapture(self.video_path)
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='./weights/luggage.pt')

        while self.running:
            ret, frame = cap.read()
            if ret:
                results = model(frame)
                results.render()  # Draw bounding boxes

                # Check for luggage ('0' class) and track time if detected
                luggage_detected = False
                for *_, conf, cls in results.xyxy[0]:
                    if conf > 0.5 and results.names[int(cls)] == '0':
                        luggage_detected = True
                        if self.detection_start_time is None:
                            self.detection_start_time = time.time()  # Start the timer
                        break  # Only track the first instance in each frame

                # If luggage has been detected for more than 10 seconds, take a screenshot and emit the dialog signal
                if luggage_detected:
                    if time.time() - self.detection_start_time > 10:
                        timestamp = self.save_detection(frame)
                        self.showDialog.emit(f"Luggage detected. Please check the timestamped screenshot: {timestamp}")
                        self.detection_start_time = None  # Reset the timer after taking the screenshot
                else:
                    self.detection_start_time = None  # Reset the timer if no luggage is detected

                # Convert to QImage for display
                height, width, channels = frame.shape
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                bytesPerLine = channels * width
                convertToQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(676, 512, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

        cap.release()
        cv2.destroyAllWindows()

    def save_detection(self, frame):
        timestamp = time.strftime("%Y%m%d-%H%M%S")  # Get current time for a unique filename
        cv_path = f"screenshots/luggage_det_{timestamp}.jpg"
        cv2.imwrite(cv_path, frame)
        print("Screenshot Saved")
        return timestamp  # Return the timestamp for the dialog box
