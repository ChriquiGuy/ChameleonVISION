from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import *
import cv2
import numpy as np
import screens.detection_window as detection_window
import screens.VideoThreadFoeMainWindow as video_thread_for_main_window

video_thread_for_main_window = video_thread_for_main_window.VideoThread


class Detection(QtWidgets.QWidget, detection_window.Ui_MainWindow):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        # create the video capture thread
        self.thread = video_thread_for_main_window()
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
        p = convert_to_Qt_format.scaled(self.VideoHolder.size().width(),
                                        self.VideoHolder.size().height())  # , Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def update_alert(self, isOut):
        if isOut:
            self.AlertText.setText("Ball Out")
            self.AlertTitle.setStyleSheet(
                "background-color: rgb(255, 0, 0);\nborder-style:outset;\nborder-radius:10px;\ncolor: rgb(250, 255, 255);\nfont: 14pt")
        else:
            self.AlertText.setText("Ball In")
            self.AlertTitle.setStyleSheet(
                "background-color: rgb(0, 255, 0);\nborder-style:outset;\nborder-radius:10px;\ncolor: rgb(250, 255, 255);\nfont: 14pt")
