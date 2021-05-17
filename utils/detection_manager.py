import cv2
import numpy as np

from PyQt5.QtCore import pyqtSignal, QThread, QObject

from utils.object_detection import ObjectDetection
from utils.field_detection import FieldDetection
from utils.event_detection import EventDetection


class Detector(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    ball_event_signal = pyqtSignal(bool, int)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.debug_flag = False
        self.calibration_flag = False
        self.play_flag = False
        
        self.field_detector = None
        self.o_detection = None
        self.event_detector = None
        
        

    def run(self):

        # Init object detection method
        self.o_detection = ObjectDetection()
        self.o_detection.initialize_model()

        # Init field detection method
        self.field_detector = FieldDetection()

        # Init event detection method
        self.event_detector = EventDetection()

        # Load RTMP
        # checkRTMP server.txt
        # cap = cv2.VideoCapture('rtmp://127.0.0.1:1935/ChameleonVISION/1234')

        # Load video
        cap = cv2.VideoCapture("./videos/volley.mp4")
        
        skip_frames = 350

        while self._run_flag:
            
            if not self.play_flag : continue
            
            ret, current_frame = cap.read()
            
            if skip_frames != 0:
                skip_frames = skip_frames -1 
                continue

            if ret:

                # Detect objects
                classes, scores, detection_boxes = self.o_detection.detect(current_frame)

                # Detect field
                LeftUp, LeftDown, RightDown, RightUp, field_center = self.field_detector.detect_field(current_frame)

                # Debug draw detections
                result_frame = current_frame.copy()

                # Detect Events
                ball_out_event, team = self.event_detector.check_ball_event(result_frame, classes, detection_boxes, LeftUp, LeftDown, RightDown, RightUp)

                # Main screen
                if self.debug_flag:

                    # Draw field
                    result_frame = self.field_detector.draw_field(result_frame)

                    # Draw object
                    result_frame = self.o_detection.draw_objects(result_frame, classes, scores, detection_boxes, field_center)

                # Calibration screen
                if self.calibration_flag:
                    result_frame = self.field_detector.calibration(result_frame)

                if ball_out_event is not None:
                    self.ball_event_signal.emit(ball_out_event, team)

                # Show to screen
                self.change_pixmap_signal.emit(result_frame)

            else:
                print("RTMP IS NOT CONNECTED")

        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
