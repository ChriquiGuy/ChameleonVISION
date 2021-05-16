from PyQt5.QtWidgets import QWidget
import time

from utils.helper import *
from utils.detection_manager import Detector
from screens.ui.UI_Game import UI_Game


class Game(QWidget, UI_Game):
    
    lastAlertTime = None

    def __init__(self, parent=None):
        super(Game, self).__init__(parent)
        self.setupUi(self)
        # create the video capture thread
        self.detector = Detector()
        self.connect_signals()
        # start the thread
        self.detector.start()
        
    def connect_signals(self):
        self.detector.change_pixmap_signal.connect(self.update_image_slot)
        self.detector.ball_event_signal.connect(self.update_alert_slot)


#### SLOTS ####

    def update_image_slot(self, cv_img):
        ## Updates the image_label with a new opencv image
        qt_img = convert_cv_qt(cv_img, self.game_view.size())
        self.game_view.setPixmap(qt_img)
    

    def update_alert_slot(self, isOut):
        
        currentAlertTime = time.time()
                
        if self.lastAlertTime is not None :
            if self.lastAlertTime + 5 < currentAlertTime :
                self.lastAlertTime = None
            else :
                self.alertPopup.alert_event_name.setText("")
                return
        
        if isOut:
            self.lastAlertTime = time.time()
            self.alertPopup.alert.show()
            self.alertPopup.alert_event_name.setText("Ball Out")
        else:
            self.lastAlertTime = time.time()
            self.alertPopup.alert.show()
            self.alertPopup.alert_event_name.setText("Ball In")