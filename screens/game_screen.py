from PyQt5.QtWidgets import QWidget
import cv2
import numpy as np
import time

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

from utils.detection_manager import Detector
from screens.ui.UI_Game import UI_Game


class Game(QWidget, UI_Game):
    
    lastAlertTime = None

    def __init__(self, parent=None):
        super(Game, self).__init__(parent)
        self.setupUi(self)

        # create the video capture thread
        self.detector = Detector()
        # connect its signal to the update_image slot
        self.detector.change_pixmap_signal.connect(self.update_image)
        self.detector.ball_out_signal.connect(self.update_alert)

        # start the thread
        self.detector.start()

    def closeEvent(self, event):
        self.detector.stop()
        event.accept()

    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.game_view.setPixmap(qt_img)
    
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.game_view.size().width(), self.game_view.size().height()) #, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def update_alert(self, isOut):
        
        currentAlertTime = time.time()
                
        if self.lastAlertTime is not None :
            if self.lastAlertTime + 5 < currentAlertTime :
                self.lastAlertTime = None
            else :
                self.alert_event_name.setText("")
                return
        
        if isOut:
            self.lastAlertTime = time.time()
            self.alert_event_name.setText("Ball Out")
        else:
            self.lastAlertTime = time.time()
            self.alert_event_name.setText("Ball In")