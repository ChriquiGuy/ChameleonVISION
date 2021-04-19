
import cv2
import numpy as np



def get_box_center(box):
   return (box[0] + int(box[2]/2), box[1] + int(box[3]/2))


def get_roi_by_delta(center, delta):
   x = center[0]
   y = center[1]
   d = delta
   return np.array([[x-d, y-d], [x-d, y+d], [x+d, y+d], [x+d, y-d]])
     
          