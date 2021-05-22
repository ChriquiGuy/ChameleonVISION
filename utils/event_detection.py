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
    last_player_touch = None
    current_player_touch = None

    def check_ball_event(self, frame, classes, boxes, LeftUp, LeftDown, RightDown, RightUp, field_center):

        # Ball
        ball_index = [index for index, object_class in enumerate(classes) if object_class == 1]
        ball = boxes[ball_index]

        # Player
        player_index = [index for index, object_class in enumerate(classes) if object_class == 0]
        playersBoxes = boxes[player_index]

        playersBoxes_ids = self.tracker.update(playersBoxes)

        # Variable to check if the ball is inside a player's BOX
        ball_inside_player = False
        self.current_player_touch = None

        for playerBox in playersBoxes_ids:

            x, y, w, h, _ = playerBox

            playerLeftUp = (x, y)
            playerLeftDown = (x, y + h)
            playerRightDown = (x + w, y + h)
            playerRightUp = (x + w, y)

            playerContour = np.array([playerLeftUp, playerLeftDown, playerRightDown, playerRightUp])
            playerContour.reshape((-1, 1, 2))
            ballInOut_playerBox = int(cv2.pointPolygonTest(playerContour, self.current_ball, True))

            # Check if ball inside the boundingBoxes of the players
            if ballInOut_playerBox >= 0:
                self.last_player_touch = (x, y, w, h)
                self.current_player_touch = self.last_player_touch
                ball_inside_player = True

                self.current_slop = None
                self.prev_slop = None
                self.prev_ball = None
                self.pre_prev_ball = None

                return None, None

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
            return None, None

        self.current_slop = self.claculate_slope(self.prev_ball, self.current_ball)
        self.prev_slop = self.claculate_slope(self.pre_prev_ball, self.prev_ball)

        FieldContour = np.array([LeftUp, LeftDown, RightDown, RightUp])
        FieldContour.reshape((-1, 1, 2))

        # Check change direction and if the ball is inside a player's BOX
        if (abs(self.current_slop) - abs(self.prev_slop) > 30) and not ball_inside_player:

            BallInOut = int(cv2.pointPolygonTest(FieldContour, self.current_ball, True))

            if BallInOut >= 0:
                # Ball In
                team = self.check_event_side(field_center, True)
                return False, team
            else:
                # Ball Out
                team = self.check_event_side(field_center, False)
                return True, team
        # No ball event
        return None, None

    def claculate_slope(self, pointA, pointB):
        slope_line = (pointA[0], pointA[1], pointB[0], pointB[1])
        slope = (180 / np.pi) * np.arctan2(slope_line[3] - slope_line[1], slope_line[2] - slope_line[0])
        return slope

    def check_event_side(self, field_center, is_ball_in):
        ball_side = self.get_object_side(self.current_ball, field_center)
        last_player_side = self.get_object_side(self.last_player_touch, field_center)

        if ball_side == last_player_side:
            return int(not ball_side)
        else:
            if is_ball_in:
                return last_player_side
            else:
                return ball_side

    def get_object_side(self, obj_point, field_center):

        if field_center and obj_point and obj_point[0] < field_center:
            return 0
        else:
            return 1

    def draw_event(self, frame, field_center):

        if self.current_ball and self.pre_prev_ball and self.pre_prev_ball:
            cv2.line(frame, (self.current_ball[0], self.current_ball[1]),
                     (self.pre_prev_ball[0], self.pre_prev_ball[1]),
                     (0, 255, 0), 4, cv2.LINE_AA)

            cv2.putText(frame, f'slop = {abs(self.current_slop) - abs(self.prev_slop)}',
                        (self.current_ball[0], self.current_ball[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        if self.current_player_touch:
            x, y, w, h = self.current_player_touch
            playerLeftUp = (x, y)
            playerRightDown = (x + w, y + h)
            cv2.rectangle(frame, playerLeftUp, playerRightDown, (0, 255, 253), 2)

        if self.current_ball and self.last_player_touch:
            ball_side = self.get_object_side(self.current_ball, field_center)
            last_player_side = self.get_object_side(self.last_player_touch, field_center)

            cv2.putText(frame, f'ball_side = {self.int_to_side(ball_side)}', (640, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            cv2.putText(frame, f'last_player_side = {self.int_to_side(last_player_side)}', (640, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        return frame

    def int_to_side(self, _int):
        if _int == 0:
            return "Left"
        else:
            return "Rigth"

    def is_in_serve_position(self, left, rigth):

        if not self.last_player_touch or left == None or rigth == None: return False
        x, y, w, h = self.last_player_touch
        playerLeftUp = (x, y)
        playerLeftDown = (x, y + h)
        playerRightDown = (x + w, y + h)
        playerRightUp = (x + w, y)

        playerContour = np.array([playerLeftUp, playerLeftDown, playerRightDown, playerRightUp])
        playerContour.reshape((-1, 1, 2))
        ballInOut_playerBox = int(cv2.pointPolygonTest(playerContour, self.current_ball, True))

        if ballInOut_playerBox >= 0 and (x < left or x > rigth):
            return True
        else:
            return False

    def check_net_touch(self, frame, NetLine):

        if NetLine is None: return
        net_slop = abs(self.claculate_slope((NetLine[0], NetLine[1]), (NetLine[2], NetLine[3])))
        if net_slop > 80:
            cv2.line(frame, (NetLine[0], NetLine[1]), (NetLine[2], NetLine[3]),
                     (0, 255, 0), 8, cv2.LINE_AA)
        elif net_slop > 75:
            cv2.line(frame, (NetLine[0], NetLine[1]), (NetLine[2], NetLine[3]),
                     (0, 0, 255), 8, cv2.LINE_AA)
            
            
            
    def reset_data(self):
        self.current_ball = None
        self.prev_ball = None
        self.pre_prev_ball = None
        self.current_slop = None
        self.prev_slop = None
        self.found_last_frame = False
        self.last_player_touch = None
        self.current_player_touch = None