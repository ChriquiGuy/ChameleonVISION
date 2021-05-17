from PyQt5.QtWidgets import QWidget
import time

from utils.helper import *
from utils.detection_manager import Detector
from screens.ui.UI_Game import UI_Game


class Game(QWidget, UI_Game):
    
    detector = None
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
        self.debug_btn.clicked.connect(self.on_debug_btn_click)
        self.calibration_btn.clicked.connect(self.on_calibration_btn_click)
        self.play_btn.clicked.connect(self.on_play_btn_click)
        self.stop_btn.clicked.connect(self.on_stop_btn_click)
        
        
    
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
            
            
    def on_debug_btn_click(self):
        self.detector.debug_flag = not self.detector.debug_flag
        self.detector.calibration_flag = False
        
    def on_calibration_btn_click(self):
        self.detector.calibration_flag = not self.detector.calibration_flag
        self.detector.debug_flag = False
        
    def on_play_btn_click(self):
        self.detector.play_flag = True
        
    def on_stop_btn_click(self):
        self.detector.play_flag = False
