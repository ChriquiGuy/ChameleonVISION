from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import cv2
import numpy as np
from utils.object_detection import ObjectDetection
from utils.field_detection import FieldDetection
from utils.event_detection import EventDetection


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    ball_out_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # Init object detection method
        o_detection = ObjectDetection()
        o_detection.initialize_model()
        detection_boxes = []

        # Init field detection method
        field_detector = FieldDetection()

        # Init event detection method
        event_detector = EventDetection()

        # capture from cam/video
        cap = cv2.VideoCapture("/home/chameleonvision/Desktop/Project/videos/videos_720p/DJI_0858_Trim.mp4")

        while self._run_flag:
            ret, current_frame = cap.read()
            # resize = cv2.resize(current_frame, (1280, 720))

            if ret:
                # Detect objects
                classes, scores, detection_boxes = o_detection.detect(current_frame)
                # Detect field
                LeftUp, LeftDown, RightDown, RightUp = field_detector.detect_field(current_frame)
                # Debug draw detections
                result_frame = current_frame.copy()
                # Draw field
                result_frame = field_detector.draw_field(result_frame, LeftUp, LeftDown, RightDown, RightUp)
                # Draw object
                result_frame = o_detection.draw_objects(result_frame, classes, scores, detection_boxes)
                # # Detect Events
                # isBallOut = event_detector.check_ball_out(result_frame, classes, detection_boxes, LeftUp, LeftDown,
                #                                           RightDown, RightUp)
                # self.ball_out_signal.emit(isBallOut)
                # # Show to screen
                self.change_pixmap_signal.emit(result_frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break

        # shut down capture system
        cap.release()
        # # Closes all the frames
        # cv2.destroyAllWindows()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()