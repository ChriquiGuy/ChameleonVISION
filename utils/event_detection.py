import os
import cv2
import numpy as np
from .helper import *

MAX_MISS_FRAMES = 30
BALL_ROI_DELTA = 50


class EventDetection():
       
   current_ball = []
   prev_ball = []
   miss_frames_count = 0


   def check_ball_out(self,frame,  classes, boxes, Leftup, LeftDown, RightDown, RightUp):
           
      # Get ball indexes in classes list
      ball_index = [index for index, object_class in enumerate(classes) if object_class == 1]
      # Get all boxes in the given indexes
      balls_list = list(map(boxes.__getitem__, ball_index))
            
      # Search for ball inside field
      current_ball = self.get_inside_ball(frame, balls_list, Leftup, LeftDown, RightDown, RightUp)
      
      # Check if no ball inside
      if(len(current_ball) == 0):
         self.miss_frames_count += 1
         if self.miss_frames_count > MAX_MISS_FRAMES : 
            self.prev_ball = []
            return True
         else : return False
         
      # Ball detected - reset miss count
      self.miss_frames_count = 0
      
      # Check if more then one ball exist
      if(len(current_ball) > 1): return False
      # If there is one ball and his inside
      else : 
         self.prev_ball = current_ball[0]
         return False

      
   def get_inside_ball(self, frame, balls_boxes, Leftup, LeftDown, RightDown, RightUp):
          
      # Create field contour
      field_contour = np.array([Leftup, LeftDown, RightDown, RightUp])
      # Find all balls inside field
      ball_inside_field = [ball for ball in balls_boxes if cv2.pointPolygonTest(field_contour, get_box_center(ball), True) > 0]
      

      # Search in prev roi incase prev exist
      if(len(self.prev_ball)):
         # Calculate prev ball roi
         prev_center = get_box_center(self.prev_ball)
         prev_roi = get_roi_by_delta(prev_center, BALL_ROI_DELTA)
         # Draw ball ROI
         frame = cv2.circle(frame, prev_center, 15, (0,0,0), 2)
         overlay = frame.copy()
         cv2.drawContours(frame,[prev_roi], 0, (150,100,255), -1)
         cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
         # Find ball inside field inside prev ball roi
         ball_inside_field = [ball for ball in ball_inside_field if cv2.pointPolygonTest(prev_roi, get_box_center(ball), True) >= 0]   
      
      return ball_inside_field
      
      

   
          




 
            







