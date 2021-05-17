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
        self.init_gamma_bar()
        self.start_timer()
        self.connect_signals()


    def hide_none_start_items(self):
        self.alert.hide()
        self.gamma_slider.hide()
        
    def init_gamma_bar(self):
        self.gamma_slider.setMinimum(0)
        self.gamma_slider.setMaximum(255)
        
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
        self.gamma_slider.valueChanged.connect(self.gamma_value_changed)
        

#### SLOTS ####

    def update_image_slot(self, cv_img):
        ## Updates the image_label with a new opencv image
        qt_img = convert_cv_qt(cv_img, self.game_view.size())
        self.game_view.setPixmap(qt_img)
    

    def update_alert_slot(self, isOut= None, team=None):
        
        currentAlertTime = time.time()
                
        if self.lastAlertTime is not None :
            if self.lastAlertTime + 5 < currentAlertTime :
                self.lastAlertTime = None
                self.alert.hide()
            else :
                return
        
        team_color = "rgb(50, 50, 200)"
        if team == 1 : team_color = "rgb(200, 50, 50)"
        self.alert_team_color.setStyleSheet(f"background-color:{team_color};\n"
                                            "border-style:outset;\n"
                                            "border-radius:10px;\n"
                                            "color: rgb(250, 255, 255);\n"
                                            "font: 14pt;")
        if isOut == True:
            self.lastAlertTime = time.time()
            self.alert_event_name.setText("Ball Out")
            self.alert.show()
            
        elif isOut == False:
            self.lastAlertTime = time.time()
            self.alert_event_name.setText("Ball In")
            self.alert.show()
  
  
              
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
        self.gamma_slider.setValue(self.detector.field_detector.Gamma_Min)
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
        self.update_alert_slot()
        
    def gamma_value_changed(self, value):
        self.detector.field_detector.Gamma_Min = int(value)