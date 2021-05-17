from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
import time
from datetime import datetime

from utils.helper import *
from utils.detection_manager import Detector
from screens.ui.UI_Game import UI_Game


class Game(QWidget, UI_Game):
    
    detector = None
    timer = None
    start_time = None
    lastAlertTime = None

    def __init__(self, parent=None):
        super(Game, self).__init__(parent)
        self.setupUi(self)
        self.hide_none_start_items()
        # create the video capture thread
        self.detector = Detector()
        # start the thread
        self.detector.start()
        self.start_timer()
        self.connect_signals()


    def hide_none_start_items(self):
        self.alert.hide()
        self.gamma_slider.hide()
        

        
    def start_timer(self):
        self.start_time = datetime.now()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)


    def connect_signals(self):
        self.detector.change_pixmap_signal.connect(self.update_image_slot)
        self.detector.ball_event_signal.connect(self.update_alert_slot)
        self.debug_btn.clicked.connect(self.on_debug_btn_click)
        self.calibration_btn.clicked.connect(self.on_calibration_btn_click)
        self.play_btn.clicked.connect(self.on_play_btn_click)
        self.stop_btn.clicked.connect(self.on_stop_btn_click)
        self.game_btn.clicked.connect(self.on_game_btn_click)
        

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
  
  
              
    def on_game_btn_click(self):
        self.detector.debug_flag = False
        self.detector.calibration_flag = False    
        self.gamma_slider.hide()      
            
            
    def on_debug_btn_click(self):
        self.detector.debug_flag = True
        self.detector.calibration_flag = False
        self.gamma_slider.hide()
        
        
    def on_calibration_btn_click(self):
        self.detector.calibration_flag = True
        self.detector.debug_flag = False
        self.gamma_slider.show()
        
        
    def on_play_btn_click(self):
        self.detector.play_flag = True
        self.timer.start(1000)
        
        
    def on_stop_btn_click(self):
        self.detector.play_flag = False
        self.timer.stop()
    
    
    def update_time(self):
        delta_time = datetime.now() - self.start_time
        game_time = time.gmtime(delta_time.total_seconds())
        game_time = time.strftime('%H:%M:%S', game_time)
        self.game_time.setText(game_time)
