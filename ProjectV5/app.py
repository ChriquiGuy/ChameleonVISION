import sys
import cv2
import numpy as np

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow

from utils.object_detection import ObjectDetection
from utils.field_detection import FieldDetection
from utils.event_detection import EventDetection
import screens.detection_window as detection_window


class VideoThread(QThread):
    
    change_pixmap_signal = pyqtSignal(np.ndarray)
    ball_out_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):

        # Init object detection method
        o_detection = ObjectDetection()
        o_detection.initialize_model()

        # Init field detection method
        field_detector = FieldDetection()
        
        # Init event detection method
        event_detector = EventDetection()

        # Load RTMP
        # cap = cv2.VideoCapture('rtmp://127.0.0.1:1935/ChameleonVISION/1234')          # checkRTMP server.txt
        cap = cv2.VideoCapture("/home/chameleonvision/Desktop/ProjectV2/videos/858.MP4")


        # change the size of video to 1280X720
        cap.set(3, 1280)
        cap.set(4, 720)
                
        while self._run_flag:
            ret, current_frame = cap.read()

            if ret:
                # Detect objects
                classes, scores, detection_boxes = o_detection.detect(current_frame)
                # Detect field
                LeftUp, LeftDown, RightDown, RightUp = field_detector.detect_field(current_frame)
                # Debug draw detections
                result_frame = current_frame.copy()

                # Draw field
                result_frame = field_detector.draw_field(result_frame, LeftUp, LeftDown, RightDown, RightUp)
                # Draw object 
                result_frame = o_detection.draw_objects(result_frame, classes, scores, detection_boxes)
                # Detect Events
                isBallOut = event_detector.check_ball_out(result_frame, classes, detection_boxes,
                                                          LeftUp, LeftDown, RightDown, RightUp)
                self.ball_out_signal.emit(isBallOut)
                # Show to screen
                self.change_pixmap_signal.emit(result_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            else:
                print("RTMP IS NOT CONNECTED")
                
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QMainWindow, detection_window.Ui_MainWindow):


    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.ball_out_signal.connect(self.update_alert)

        # start the thread
        self.thread.start()


    def closeEvent(self, event):
        self.thread.stop()
        event.accept()


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.VideoHolder.setPixmap(qt_img)
    
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.VideoHolder.size().width(), self.VideoHolder.size().height()) #, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


    def update_alert(self, isOut):
        if isOut:
            self.AlertText.setText("Ball Out")
            self.AlertTitle.setStyleSheet("background-color: rgb(255, 0, 0);\nborder-style:outset;\nborder-radius:10px;\ncolor: rgb(250, 255, 255);\nfont: 14pt")
        else:
            self.AlertText.setText("Ball In")
            self.AlertTitle.setStyleSheet("background-color: rgb(0, 255, 0);\nborder-style:outset;\nborder-radius:10px;\ncolor: rgb(250, 255, 255);\nfont: 14pt")
        
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
