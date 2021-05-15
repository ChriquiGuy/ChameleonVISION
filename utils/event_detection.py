import os
import cv2
import numpy as np
from .helper import *


class EventDetection:
    current_ball = None
    prev_ball = None
    pre_prev_ball = None
    current_slop = None
    prev_slop = None
    found_last_frame = False

    def check_ball_out(self, frame, classes, boxes, LeftUp, LeftDown, RightDown, RightUp):

        # Variable to check if the ball is inside a player's BOX
        ballBox = 0

        # Ball
        ball_index = [index for index, object_class in enumerate(classes) if object_class == 1]
        ball = boxes[ball_index]

        # Player
        player_index = [index for index, object_class in enumerate(classes) if object_class == 0]
        playersBoxes = boxes[player_index]

        for playerBox in playersBoxes:
            playerLeftUp = (playerBox[0], playerBox[1])
            playerLeftDown = (playerBox[0], playerBox[1] + playerBox[3])
            playerRightDown = (playerBox[0] + playerBox[2], playerBox[1] + playerBox[3])
            playerRightUp = (playerBox[0] + playerBox[2], playerBox[1])

            # See players bounding boxes for debug
            cv2.rectangle(frame, playerLeftUp, playerRightDown, (0, 0, 0), 1)

            playerContour = np.array([playerLeftUp, playerLeftDown, playerRightDown, playerRightUp])

            playerContour.reshape((-1, 1, 2))

            ballInOut_playerBox = int(cv2.pointPolygonTest(playerContour, self.current_ball, True))

            # Check if ball inside the boundingBoxes of the players
            if ballInOut_playerBox >= 0:
                ballBox += 1

            print(ballBox)

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
                 (0, 0, 255), 4, cv2.LINE_AA)

        self.current_slop = self.claculate_ball_slope(self.prev_ball, self.current_ball)
        self.prev_slop = self.claculate_ball_slope(self.pre_prev_ball, self.prev_ball)
        FieldContour = np.array([LeftUp, LeftDown, RightDown, RightUp])
        FieldContour.reshape((-1, 1, 2))

        # Check change direction and if the ball is inside a player's BOX
        if (self.current_slop != self.prev_slop) and (ballBox == 0):

            BallInOut = int(cv2.pointPolygonTest(FieldContour, self.current_ball, True))

            # Ball In
            if BallInOut >= 0:
                cv2.putText(frame, "BALL IN", (25, 25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 3)
                return False
            else:
                # Ball Out
                cv2.putText(frame, "BALL OUT :" + str(abs(BallInOut)) + "cm", (25, 25),
                            cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 3)
                return True
        return None

    def claculate_ball_slope(self, pointA, pointB):
        if (pointA[0] - pointB[0]) == 0:
            return 0

        return int((pointA[1] - pointB[1]) / (pointA[0] - pointB[0]))

    # def check_ball_out(self,frame,  classes, boxes, Leftup, LeftDown, RightDown, RightUp):

    #    # Get ball indexes in classes list
    #    ball_index = [index for index, object_class in enumerate(classes) if object_class == 1]
    #    # Get all boxes in the given indexes
    #    balls_list = list(map(boxes.__getitem__, ball_index))
    #    # Search for ball inside field
    #    current_ball = self.get_inside_ball(frame, balls_list, Leftup, LeftDown, RightDown, RightUp)
    #    #self.if_player_touch(classes,boxes,current_ball,Leftup, LeftDown, RightDown, RightUp)
    #    # Check if no ball inside
    #    if(len(current_ball) == 0):
    #       self.miss_frames_count += 1
    #       if self.miss_frames_count > MAX_MISS_FRAMES:
    #          self.prev_ball = []
    #          return True
    #       else : return False

    #    # Ball detected - reset miss count
    #    self.miss_frames_count = 0

    #    # Check if more then one ball exist
    #    if(len(current_ball) > 1): return False
    #    # If there is one ball and his inside
    #    else :
    #       self.prev_ball = current_ball[0]
    #       return False

    # def if_player_touch(self, classes, boxes ,current_ball, Leftup, LeftDown, RightDown, RightUp):
    #    # center_up = (Leftup[0]+RightUp[0])/2
    #    # center_down = (LeftDown[0]+RightDown[0])/2
    #    current_ball_center = ()
    #    if current_ball_center:
    #       current_ball_center = get_box_center(current_ball)
    #    for box in boxes:
    #       box = np.array(box)
    #       if current_ball.__sizeof__() != 0:
    #          player_touch = cv2.pointPolygonTest(box, current_ball_center, True)
    #          if player_touch >= 0:
    #             print(player_touch)

    # def get_inside_ball(self, frame, balls_boxes, Leftup, LeftDown, RightDown, RightUp):

    #    # Create field contour
    #    field_contour = np.array([Leftup, LeftDown, RightDown, RightUp])
    #    # Find all balls inside field
    #    ball_inside_field = [ball for ball in balls_boxes if cv2.pointPolygonTest(field_contour, get_box_center(ball), True) > 0]

    #    # Search in prev roi incase prev exist
    #    if(len(self.prev_ball)):
    #       # Calculate prev ball roi
    #       prev_center = get_box_center(self.prev_ball)
    #       prev_roi = get_roi_by_delta(prev_center, BALL_ROI_DELTA)
    #       # Draw ball ROI
    #       frame = cv2.circle(frame, prev_center, 15, (0,0,0), 2)
    #       overlay = frame.copy()
    #       cv2.drawContours(frame,[prev_roi], 0, (150,100,255), -1)
    #       cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    #       # Find ball inside field inside prev ball roi
    #       ball_inside_field = [ball for ball in ball_inside_field if cv2.pointPolygonTest(prev_roi, get_box_center(ball), True) >= 0]

    #    return ball_inside_field

    # def get_player_inside_filed(self, frame, player_boxes, Leftup, LeftDown, RightDown, RightUp):
    #    # Create field contour
    #    field_contour = np.array([Leftup, LeftDown, RightDown, RightUp])
    #    # Find all balls inside field
    #    player_inside_field = [player for player in player_boxes if cv2.pointPolygonTest(field_contour, get_box_center(player), True) > 0]
    #    if len(player_inside_field):
    #       for player in player_boxes:
    #          player_center = get_box_center(player)
    #          prev_roi = get_roi_by_delta(player_center, BALL_ROI_DELTA) # maybe change the delta of ROI
    #          # Draw ball ROI
    #          frame = cv2.rectangle(frame, player_center, 15, (0, 0, 0), 2)
    #          overlay = frame.copy()
    #          cv2.drawContours(frame, [prev_roi], 0, (150, 100, 255), -1)
    #          cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    #          # Find ball inside field inside prev ball roi
    #          ball_inside_field = [player_one for player_one in player_boxes if
    #                               cv2.pointPolygonTest(prev_roi, get_box_center(player_one), True) >= 0]
