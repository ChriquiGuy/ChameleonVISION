import cv2
import numpy as np
# import time

# includes
from PyQt5.QtCore import pyqtSignal, QThread, QObject
from tools.object_detection import ObjectDetection
from tools.field_detection import FieldDetection
from tools.event_detection import EventDetection
from tools.replay_manager import ReplayManager
from tools.object_tracker import ObjectTracker
from tools.ball_tracker import BallTracker
# from utils.stream_stabilizer import StreamStabilizer


class Detector(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    ball_event_signal = pyqtSignal(bool, int)
    in_serve_position = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.tracker = ObjectTracker()
        self.ballTracker = BallTracker()

        self._run_flag = True
        self.debug_flag = False
        self.calibration_flag = False
        self.play_flag = False
        self.switch_flag = False
        self.replay_flag = False

        self.field_detector = None
        self.o_detection = None
        self.event_detector = None
        self.stabilizer = None
        self.replayManager = None
        self.cap = None

    def run(self):

        # Init methods
        # self.stabilizer = StreamStabilizer()
        self.replayManager = ReplayManager()
        self.o_detection = ObjectDetection()
        self.o_detection.initialize_model()
        self.field_detector = FieldDetection()
        self.event_detector = EventDetection()

        # Load RTMP
        # checkRTMP server.txt
        # cap = cv2.VideoCapture('rtmp://127.0.0.1:1935/ChameleonVISION/1234')

        # Load video
        self.cap = cv2.VideoCapture("./videos/volley.mp4")

        # Jump to first alert
        # self.cap.set(cv2.CAP_PROP_POS_FRAMES, 500)

        while self._run_flag:

            if self.replay_flag:
                continue
            elif self.replayManager.replay_end_frame:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.replayManager.replay_end_frame)
                self.replayManager.replay_end_frame = None
                self.event_detector.reset_data()

            if not self.play_flag:
                continue

            ret, current_frame = self.cap.read()

            # current_frame = self.stabilizer.stabilizer_frame(current_frame)

            if ret:

                # time.sleep(0.01)

                # Detect objects
                classes, scores, detection_boxes = self.o_detection.detect(current_frame)

                # Detect field
                LeftUp, LeftDown, RightDown, RightUp, NetLine, field_center, field_contour = \
                    self.field_detector.detect_field(current_frame)

                # Debug draw detections
                result_frame = current_frame.copy()

                # Ball tracker
                ball_box = self.ballTracker.track_inside_field(classes, detection_boxes, field_contour)

                # Players tracker
                # if field_contour is not None:
                #     objects_bbs_ids = self.tracker.track_inside_field(result_frame, classes,
                #                                                       scores, detection_boxes,
                #                                                       field_contour)

                # Detect Events
                result_frame, ball_out_event, team = self.event_detector.check_ball_event(result_frame,
                                                                                          classes, detection_boxes,
                                                                                          field_contour, ball_box,
                                                                                          field_center)
                if self.switch_flag:
                    team = not team

                serve_event = None
                if LeftUp and RightUp:
                    serve_event = self.event_detector.is_in_serve_position(LeftUp[0], RightUp[0])

                # Main screen
                if self.debug_flag:
                    # Draw field
                    result_frame = self.field_detector.draw_field(result_frame)

                    # Draw objects
                    result_frame = self.o_detection.draw_objects(result_frame, classes, scores, detection_boxes,
                                                                 field_center, LeftUp, LeftDown, RightDown, RightUp)

                    # # Draw tracking
                    # result_frame = self.o_detection.draw_tracking(result_frame, objects_bbs_ids, ball_box)

                    # Draw ball slop
                    result_frame = self.event_detector.draw_event(result_frame, field_center)

                # Calibration screen
                if self.calibration_flag:
                    result_frame = self.field_detector.calibration(result_frame)

                # Draw events (GUI)
                if ball_out_event is not None and team is not None:
                    self.ball_event_signal.emit(ball_out_event, team)

                if serve_event:
                    self.in_serve_position.emit()

                # self.event_detector.check_net_touch(result_frame, NetLine)

                # Show to screen
                self.change_pixmap_signal.emit(result_frame)

            else:
                print("RTMP IS NOT CONNECTED")

        # shut down capture system
        self.cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
