import sys
import cv2
import numpy as np

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout , QPushButton, QHBoxLayout, QMainWindow

from utils.object_detection import ObjectDetection
from utils.field_detection import FieldDetection
from utils.event_detection import EventDetection
import app_test



class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    ball_out_signal = pyqtSignal(bool)


    def __init__(self):
        super().__init__()
        self._run_flag = True
        pts = []

    def run(self):

        # Init object detection method
        o_detection = ObjectDetection()
        o_detection.initialize_model()
        o_detection_frame = None
        detection_boxes = []
        


        # Init field detection method
        field_detector = FieldDetection()
        event_detector = EventDetection()

        # capture from web cam
        cap = cv2.VideoCapture("/home/chameleonvision/Desktop/Project/videos/818.MP4")
        pts = []
        while self._run_flag:
            ret, current_frame = cap.read()

            if ret:
                # Detect objects
                classes, scores, detection_boxes = o_detection.detect(current_frame.copy())
                # Detect field
                Leftup, LeftDown, RightDown, RightUp = field_detector.detect_field(current_frame.copy())
                
                result_frame = None
                # Draw field
                result_frame = field_detector.draw_field(current_frame.copy(), Leftup, LeftDown, RightDown, RightUp)
                # Draw object 
                result_frame = o_detection.draw_objects(result_frame, classes, scores, detection_boxes)

                # Detect Events
                isBallOut = event_detector.check_ball_out(result_frame, classes, detection_boxes, Leftup, LeftDown, RightDown, RightUp)
                self.ball_out_signal.emit(isBallOut)
                
                # Show to screen
                self.change_pixmap_signal.emit(result_frame)
                

        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QMainWindow, app_test.Ui_MainWindow):


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
        p = convert_to_Qt_format.scaled(self.VideoHolder.size().width() , self.VideoHolder.size().height()) #, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    @pyqtSlot(bool)
    def update_alert(self, isOut):
        if isOut :
            self.AlertText.setText("Ball Out")
            self.AlertTitle.setStyleSheet("background-color: rgb(255, 0, 0);\nborder-style:outset;\nborder-radius:10px;\ncolor: rgb(250, 255, 255);\nfont: 14pt")
        else :
            self.AlertText.setText("Ball In")
            self.AlertTitle.setStyleSheet("background-color: rgb(0, 255, 0);\nborder-style:outset;\nborder-radius:10px;\ncolor: rgb(250, 255, 255);\nfont: 14pt")
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
