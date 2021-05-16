
import cv2
import numpy as np

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap


def get_box_center(box):
   return (box[0] + int(box[2]/2), box[1] + int(box[3]/2))


def get_roi_by_delta(center, delta):
   x = center[0]
   y = center[1]
   d = delta
   return np.array([[x-d, y-d], [x-d, y+d], [x+d, y+d], [x+d, y-d]])
     
     
     
def convert_cv_qt(cv_img, game_view_size):
   """Convert from an opencv image to QPixmap"""
   rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
   h, w, ch = rgb_image.shape
   bytes_per_line = ch * w
   convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
   p = convert_to_Qt_format.scaled(game_view_size.width(), game_view_size.height()) #, Qt.KeepAspectRatio)
   return QPixmap.fromImage(p)