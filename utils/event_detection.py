import cv2
import numpy as np
from .helper import *
from .object_tracker import ObjectTracker


class EventDetection:
    tracker = ObjectTracker()

    current_ball = None
    prev_ball = None
    pre_prev_ball = None
    current_slop = None
    prev_slop = None
    found_last_frame = False

    def check_ball_event(self, frame, classes, boxes, LeftUp, LeftDown, RightDown, RightUp):

        # Variable to check if the ball is inside a player's BOX
        ballBox = 0

        # Ball
        ball_index = [index for index, object_class in enumerate(classes) if object_class == 1]
        ball = boxes[ball_index]

        # Player
        player_index = [index for index, object_class in enumerate(classes) if object_class == 0]
        playersBoxes = boxes[player_index]

        playersBoxes_ids = self.tracker.update(playersBoxes)

        for playerBox in playersBoxes_ids:

            x, y, w, h, playerIndex = playerBox

            playerLeftUp = (x, y)
            playerLeftDown = (x, y + h)
            playerRightDown = (x + w, y + h)
            playerRightUp = (x + w, y)

            playerContour = np.array([playerLeftUp, playerLeftDown, playerRightDown, playerRightUp])
            playerContour.reshape((-1, 1, 2))
            ballInOut_playerBox = int(cv2.pointPolygonTest(playerContour, self.current_ball, True))

            # Check if ball inside the boundingBoxes of the players
            if ballInOut_playerBox >= 0:
                ballBox += 1

        # If ball was found
        if len(ball) == 1:
            self.found_last_frame = not self.found_last_frame
            ball_center = get_box_center(ball[0])
            if self.found_last_frame:
                self.pre_prev_ball = self.prev_ball
                self.prev_ball = self.current_ball
            self.current_ball = ball_center

        # Check if ball was found before
        if self.current_ball is None or self.prev_ball is None or self.pre_prev_ball is None:
            return None

        cv2.line(frame, (self.current_ball[0], self.current_ball[1]), (self.pre_prev_ball[0], self.pre_prev_ball[1]),
                 (0, 255, 0), 4, cv2.LINE_AA)

        self.current_slop = self.claculate_ball_slope(self.prev_ball, self.current_ball)
        self.prev_slop = self.claculate_ball_slope(self.pre_prev_ball, self.prev_ball)
        FieldContour = np.array([LeftUp, LeftDown, RightDown, RightUp])
        FieldContour.reshape((-1, 1, 2))

        # Check change direction and if the ball is inside a player's BOX
        if (self.current_slop != self.prev_slop) and (ballBox == 0):

            BallInOut = int(cv2.pointPolygonTest(FieldContour, self.current_ball, True))

            if BallInOut >= 0:
                # Ball In
                return False
            else:
                # Ball Out
                return True
        # No ball event
        return None

    def claculate_ball_slope(self, pointA, pointB):
        if (pointA[0] - pointB[0]) == 0:
            return 0

        return int((pointA[1] - pointB[1]) / (pointA[0] - pointB[0]))
