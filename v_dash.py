from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import cv2
import torch
import time

class V_Dash(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self):
        super(V_Dash, self).__init__()
        self.running = True
        self.last_update_time = time.time()
    def setVideoPath(self, path):
        self.video_path = path
    def run(self):
        #cap = cv2.VideoCapture('./video/car.mp4')
        cap = cv2.VideoCapture(self.video_path)
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='./weights/car.pt')
        car_count = 0

        while self.running:
            ret, frame = cap.read()
            if ret:
                results = model(frame)
                results.render()  # Draw bounding boxes
            

                # Update car count every 10 seconds
                if time.time() - self.last_update_time > 5:
                    # Count only detections with confidence > 0.5
                    car_count = sum(1 for *_, conf, cls in results.xyxy[0] if conf > 0 and results.names[int(cls)] == '0')
                    self.last_update_time = time.time()

                # Add text for car count with a dark blue background
                text = f'Cars: {car_count}'
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                font_thickness = 2

                # Get the text size
                text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

                # Set coordinates for the text and background
                text_x = 10
                text_y = 30
                background_coords = (text_x, text_y - text_size[1] - 5, text_x + text_size[0] + 5, text_y + 5)

                # Draw dark blue background rectangle
                cv2.rectangle(frame, (background_coords[0], background_coords[1]), (background_coords[2], background_coords[3]), (0, 0, 139), -1)

                # Add text on top of the background
                cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

                # Convert to QImage for display
                height, width, channels = frame.shape
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                bytesPerLine = channels * width
                convertToQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(676, 512, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

        cap.release()
        cv2.destroyAllWindows()
