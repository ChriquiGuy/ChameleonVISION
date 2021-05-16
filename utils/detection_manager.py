import cv2
import numpy as np

from PyQt5.QtCore import pyqtSignal, QThread, QObject

from utils.object_detection import ObjectDetection
from utils.field_detection import FieldDetection
from utils.event_detection import EventDetection


class Detector(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    ball_event_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.debug_flag = False
        self.calibration_flag = True

    def run(self):

        # Init object detection method
        o_detection = ObjectDetection()
        o_detection.initialize_model()

        # Init field detection method
        field_detector = FieldDetection()

        # Init event detection method
        event_detector = EventDetection()

        # Load RTMP
        # checkRTMP server.txt
        # cap = cv2.VideoCapture('rtmp://127.0.0.1:1935/ChameleonVISION/1234')

        # Load video
        cap = cv2.VideoCapture("./videos/volley.mp4")

        while self._run_flag:
            ret, current_frame = cap.read()

            if ret:

                # Detect objects
                classes, scores, detection_boxes = o_detection.detect(current_frame)

                # Detect field
                LeftUp, LeftDown, RightDown, RightUp, field_center = field_detector.detect_field(current_frame)

                # Debug draw detections
                result_frame = current_frame.copy()

                # Detect Events
                isBallOut = event_detector.check_ball_event(result_frame, classes, detection_boxes, LeftUp, LeftDown,
                                                            RightDown, RightUp)

                # Main screen
                if self.debug_flag:

                    # Draw field
                    result_frame = field_detector.draw_field(result_frame)

                    # Draw object
                    result_frame = o_detection.draw_objects(result_frame, classes, scores, detection_boxes,
                                                            field_center)

                # Calibration screen
                if self.calibration_flag:
                    result_frame = field_detector.calibration(result_frame)

                if isBallOut is not None:
                    self.ball_event_signal.emit(isBallOut)

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
