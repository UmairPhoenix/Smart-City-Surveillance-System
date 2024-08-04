from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import cv2
import torch

class P_Dash(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self):
        super(P_Dash, self).__init__()
        self.running = True
    def setVideoPath(self, path):
        self.video_path = path
    def run(self):
        #cap = cv2.VideoCapture(self.video_path)
        #cap = cv2.VideoCapture('./video/parking.mp4')
        cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture(0 if self.video_path is None else self.video_path)
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='./weights/parking.pt')

        while self.running:
            ret, frame = cap.read()
            if ret:
                results = model(frame)

                # Manually draw bounding boxes without labels
                for *box, conf, cls in results.xyxy[0]:
                    if conf > 0.4:
                        color = (0, 255, 0) if results.names[int(cls)] == 'Empty' else (0, 0, 255)
                        cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2)

                # Count the instances of each class with confidence > 0.5
                empty_slots = sum(1 for *_, conf, cls in results.xyxy[0] if conf > 0.4 and results.names[int(cls)] == 'Empty')
                
                # Prepare text for available spaces
                text = f'Available Spaces: {empty_slots}'
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                font_thickness = 2

                # Get the text size
                text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

                # Set the coordinates for the text and background
                text_x = 10
                text_y = 30
                background_coords = (text_x, text_y - text_size[1] - 5, text_x + text_size[0] + 5, text_y + 5)

                # Draw light blue background rectangle
                # Draw dark blue background rectangle
                cv2.rectangle(frame, (background_coords[0], background_coords[1]), (background_coords[2], background_coords[3]), (0, 0, 139), -1)

                
                # Add text on top of the background
                cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

                # Convert to QImage for display
                height, width, channels = frame.shape
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                bytesPerLine = channels * width
                convertToQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(676, 468, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

        cap.release()
        cv2.destroyAllWindows()
