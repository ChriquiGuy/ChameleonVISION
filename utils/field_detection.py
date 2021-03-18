import cv2
import numpy as np
from numba import cuda


class FieldDetection():

    UpLine = None
    LeftLine = None
    DownLine = None
    RightLine = None
    NetLine = None

    Gamma_Min = 30
    
    def init_frame(self, frame):
        # Gray
        current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
        current_frame_copy = frame.copy()
        # Threshold
        res, binary = cv2.threshold(current_frame_gray, self.Gamma_Min, 255, cv2.THRESH_BINARY)     
        dilate = cv2.erode(binary, (755, 3), iterations=3)
        # Canny algorithm
        edges = cv2.Canny(binary, 1, 255) 
        return edges

    def detect_lines(self, frame):
        # HoughLinesP
        lines = cv2.HoughLinesP(frame, 1, np.pi / 180, 7, np.array([]), 500, 100)     
            
        if lines is not None:
            for i in range(0, len(lines)):
                x1, y1, x2, y2 = lines[i][0]
                # Net detect
                if (750 < x1 < 1300) & (750 < x2 < 1300):
                    self.NetLine = [(lines[i][0])]
                # Up line
                elif (0 < y1 < 400) & (0 < y2 < 400):
                    self.UpLine = [(lines[i][0])]
                # Left line
                elif (0 < x1 < 500) & (0 < x2 < 500):
                    self.LeftLine = [(lines[i][0])]
                # Down line
                elif (750 < y1 < 1000) & (750 < y2 < 1000):
                    self.DownLine = [(lines[i][0])]
                # Right line
                elif (1500 < x1 < 1850) & (1500 < x2 < 1850):
                    self.RightLine = [(lines[i][0])]

    def detect_field(self, frame):

        while(True):
            tryFrame = self.init_frame(frame)
            self.detect_lines(tryFrame)

            try:
                if self.UpLine and self.LeftLine:
                    # Left up corner
                    Leftup = self.line_intersection(self.UpLine[0], self.LeftLine[0])
                if self.DownLine and self.LeftLine:
                    # Left down corner
                    LeftDown = self.line_intersection(self.DownLine[0], self.LeftLine[0])
                if self.DownLine and self.RightLine:
                    # Right down corner
                    RightDown = self.line_intersection(self.DownLine[0], self.RightLine[0])
                if self.UpLine and self.RightLine:
                    # Right up corner
                    RightUp = self.line_intersection(self.UpLine[0], self.RightLine[0])

                return Leftup, LeftDown, RightDown, RightUp

            except NameError:
                self.Gamma_Min = self.Gamma_Min + 1
                print("Current Gamma = " + str(self.Gamma_Min))
                if(self.Gamma_Min > 255) : self.Gamma_Min = 0

    def draw_field(self, frame, Leftup, LeftDown, RightDown, RightUp):

        # Polygon corner points coordinates
        pts = np.array([Leftup, LeftDown, RightDown, RightUp])
        overlay = frame.copy()
        cv2.drawContours(overlay,[pts], 0, (255,0,255), -1)
        cv2.addWeighted(overlay, 0.2, frame, 1, 0, frame)

        return frame;


    def det(self, a, b):
        return a[0] * b[1] - a[1] * b[0]


    def line_intersection(self, line1, line2):

        x1, y1, x2, y2 = line1
        a1, b1, a2, b2 = line2
        
        xdiff = (x1 - x2, a1 - a2)
        ydiff = (y1 - y2, b1 - b2)

        div = self.det(xdiff, ydiff)
        if div == 0: raise Exception('lines do not intersect')

        d = (self.det((x1, y1), (x2, y2)), self.det((a1, b1), (a2, b2)))
        x = self.det(d, xdiff) / div
        y = self.det(d, ydiff) / div
        return int(x), int(y)
