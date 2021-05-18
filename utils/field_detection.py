import cv2
import numpy as np
from .helper import *

WEIGHT_OF_SCREEN = 1274
HEIGHT_OF_SCREEN = 720

# Net Line
NTL = WEIGHT_OF_SCREEN * 0.35  # left threshold of net
NTR = WEIGHT_OF_SCREEN * 0.65  # right threshold of net

# Left line
LTL = WEIGHT_OF_SCREEN * 0.1  # left threshold of left line
LTR = WEIGHT_OF_SCREEN * 0.3  # right threshold of left line

# Right line
RTL = WEIGHT_OF_SCREEN * 0.8  # left threshold of right line
RTR = WEIGHT_OF_SCREEN * 0.95  # right threshold of right line

# Up line
UTT = HEIGHT_OF_SCREEN * 0.1  # up threshold of top line
DTT = HEIGHT_OF_SCREEN * 0.35  # down threshold of top line

# Bottom Line
UTB = HEIGHT_OF_SCREEN * 0.7  # up threshold of Bottom line
DTB = HEIGHT_OF_SCREEN * 0.95  # down threshold of Bottom line


class FieldDetection:
    UpLine = None
    LeftLine = None
    DownLine = None
    RightLine = None
    NetLine = None
    field_center = None

    LeftUp = None
    LeftDown = None
    RightUp = None
    RightDown = None
    Gamma_Min = 51

    def init_frame(self, frame):
        current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Threshold
        res, binary = cv2.threshold(current_frame_gray, self.Gamma_Min, 255, cv2.THRESH_BINARY)
        # Canny algorithm
        edges = cv2.Canny(binary, 1, 255)
        return edges

    def detect_lines(self, edges):

        # get the lines of te field
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 7, np.array([]), 200, 100)

        if lines is not None:
            slopeLines = self.SlopeCalc(lines)
            self.NetLine = self.LinesFilter(slopeLines, NTL, NTR, 0, 2, True)
            self.UpLine = self.LinesFilter(slopeLines, UTT, DTT, 1, 3, False)
            self.LeftLine = self.LinesFilter(slopeLines, LTL, LTR, 0, 2, True)
            self.DownLine = self.LinesFilter(slopeLines, UTB, DTB, 1, 3, False)
            self.RightLine = self.LinesFilter(slopeLines, RTL, RTR, 0, 2, True)

    def detect_field(self, frame):
        edges = self.init_frame(frame)
        self.detect_lines(edges)
        try:

            if self.UpLine is not None and self.LeftLine is not None:
                # Left up corner
                self.LeftUp = self.line_intersection(self.UpLine, self.LeftLine)

            if self.DownLine is not None and self.LeftLine is not None:
                # Left down corner
                self.LeftDown = self.line_intersection(self.DownLine, self.LeftLine)

            if self.DownLine is not None and self.RightLine is not None:
                # Right down corner
                self.RightDown = self.line_intersection(self.DownLine, self.RightLine)

            if self.UpLine is not None and self.RightLine is not None:
                # Right up corner
                self.RightUp = self.line_intersection(self.UpLine, self.RightLine)
            
            if self.NetLine:
                self.field_center = (self.NetLine[0] + self.NetLine[2]) // 2

            return self.LeftUp, self.LeftDown, self.RightDown, self.RightUp, self.field_center

        except NameError:
            print("FieldDetection.detect_field: error occurred")

    def det(self, a, b):
        return a[0] * b[1] - a[1] * b[0]

    def line_intersection(self, line1, line2):

        x1, y1, x2, y2 = line1
        a1, b1, a2, b2 = line2

        xdiff = (x1 - x2, a1 - a2)
        ydiff = (y1 - y2, b1 - b2)

        try:
            div = self.det(xdiff, ydiff)
            if div == 0:
                print("lines do not intersect")
                # raise Exception('lines do not intersect')
            else:
                d = (self.det((x1, y1), (x2, y2)), self.det((a1, b1), (a2, b2)))
                x = self.det(d, xdiff) / div
                y = self.det(d, ydiff) / div
                return int(x), int(y)
        except NameError:
            print("lines do not intersect")

    def SlopeCalc(self, lines):
        Angle_Sum = np.array([(180 / np.pi) * np.arctan2(lines[:, :, 3] - lines[:, :, 1],
                                                         lines[:, :, 2] - lines[:, :, 0])])
        Angle_Sum = Angle_Sum.reshape(Angle_Sum.shape[1], Angle_Sum.shape[0], Angle_Sum.shape[2])
        slopeLines = np.append(lines, Angle_Sum, axis=2)
        return slopeLines

    def LinesFilter(self, slopeLines, threshold1, threshold2, x, y, isVertical):

        if isVertical:
            slopeLines = slopeLines[slopeLines[..., 4] > 70]  # slope
        else:
            slopeLines = slopeLines[slopeLines[..., 4] < 5]  # slope

        if slopeLines is not None:
            slopeLines = slopeLines[slopeLines[..., x] > threshold1]  # x1
        if slopeLines is not None:
            slopeLines = slopeLines[slopeLines[..., x] < threshold2]  # x1
        if slopeLines is not None:
            slopeLines = slopeLines[slopeLines[..., y] > threshold1]  # x2
        if slopeLines is not None:
            slopeLines = slopeLines[slopeLines[..., y] < threshold2]  # x2

        if len(slopeLines) >= 1:
            X1 = np.mean(slopeLines[..., 0])  # x1
            X2 = np.mean(slopeLines[..., 2])  # y1
            Y1 = np.mean(slopeLines[..., 1])  # x2
            Y2 = np.mean(slopeLines[..., 3])  # y2
            avgLine = int(X1), int(Y1), int(X2), int(Y2)
            return avgLine

    def draw_field(self, frame):
        # Polygon corner points coordinates
        if self.LeftUp is None or self.LeftDown is None or self.RightDown is None or self.RightUp is None:
            return frame

        FieldContour = np.array([self.LeftUp, self.LeftDown, self.RightDown, self.RightUp])
        FieldContour.reshape((-1, 1, 2))
        overlay = frame.copy()
        cv2.drawContours(overlay, [FieldContour], 0, (255, 0, 255), -1)
        cv2.addWeighted(overlay, 0.2, frame, 1, 0, frame)
        return frame


    def draw_field_lines(self, frame):
        if self.NetLine is not None:
            cv2.line(frame, (self.NetLine[0], self.NetLine[1]), (self.NetLine[2], self.NetLine[3]),
                     (0, 255, 0), 8, cv2.LINE_AA)

        if self.UpLine is not None:
            cv2.line(frame, (self.UpLine[0], self.UpLine[1]), (self.UpLine[2], self.UpLine[3]),
                     (0, 128, 255), 8, cv2.LINE_AA)

        if self.LeftLine is not None:
            cv2.line(frame, (self.LeftLine[0], self.LeftLine[1]), (self.LeftLine[2], self.LeftLine[3]),
                     (0, 255, 255), 8, cv2.LINE_AA)

        if self.DownLine is not None:
            cv2.line(frame, (self.DownLine[0], self.DownLine[1]), (self.DownLine[2], self.DownLine[3]),
                     (255, 255, 0), 8, cv2.LINE_AA)

        if self.RightLine is not None:
            cv2.line(frame, (self.RightLine[0], self.RightLine[1]), (self.RightLine[2], self.RightLine[3]),
                     (255, 128, 128), 8, cv2.LINE_AA)


    def calibration(self, frame):

        # Current frame
        frame_copy = frame.copy()
        current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Threshold frame
        res, binary = cv2.threshold(current_frame_gray, self.Gamma_Min, 255, cv2.THRESH_BINARY)

        # Edges frame
        edges = cv2.Canny(binary, 1, 255)
       
        # draw lines
        self.draw_field_lines(frame_copy)
        
        field = self.draw_field(frame)

        imgStack = stackImages(0.5, ([field, frame_copy], [binary, edges]))

        return imgStack
