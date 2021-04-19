import cv2
import numpy as np

WEIGHT_OF_SCREEN = 1274
HEIGHT_OF_SCREEN = 720

# Field parameters
LeftUp = (351, 231)
LeftDown = (385, 869)
RightDown = (1629, 850)
RightUp = (1608, 231)
FieldContour = np.array([LeftUp, LeftDown, RightDown, RightUp])

# Net Line
LN = WEIGHT_OF_SCREEN * 0.35  # left threshold of net
RN = WEIGHT_OF_SCREEN * 0.65  # right threshold of net

# Left line
LL = WEIGHT_OF_SCREEN * 0.1   # left threshold of left line
RL = WEIGHT_OF_SCREEN * 0.3   # right threshold of left line

# Right line
LR = WEIGHT_OF_SCREEN * 0.8   # left threshold of right line
RR = WEIGHT_OF_SCREEN * 0.95  # right threshold of right line

# Up line
UT = HEIGHT_OF_SCREEN * 0.1   # up threshold of top line
DT = HEIGHT_OF_SCREEN * 0.35  # down threshold of top line

# Bottom Line
UB = HEIGHT_OF_SCREEN * 0.7   # up threshold of Bottom line
DB = HEIGHT_OF_SCREEN * 0.95  # down threshold of Bottom line


class FieldDetection:

    UpLine = None
    LeftLine = None
    DownLine = None
    RightLine = None
    NetLine = None
    Gamma_Min = 0
    
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
            self.NetLine = self.LinesFilter(slopeLines, LN, RN)
            self.UpLine = self.LinesFilter(slopeLines, UT, DT)
            self.LeftLine = self.LinesFilter(slopeLines, LL, RL)
            self.DownLine = self.LinesFilter(slopeLines, UB, DB)
            self.RightLine = self.LinesFilter(slopeLines, LR, RR)

    def detect_field(self, frame):
            LeftUp, LeftDown, RightDown, RightUp = 0, 0, 0, 0
            edges = self.init_frame(frame)
            self.detect_lines(edges)
            try:
                if self.UpLine is not None and self.LeftLine is not None:
                    # Left up corner
                    LeftUp = self.line_intersection(self.UpLine, self.LeftLine)

                if self.DownLine is not None and self.LeftLine is not None:
                    # Left down corner
                    LeftDown = self.line_intersection(self.DownLine, self.LeftLine)

                if self.DownLine is not None and self.RightLine is not None:
                    # Right down corner
                    RightDown = self.line_intersection(self.DownLine, self.RightLine)

                if self.UpLine is not None and self.RightLine is not None:
                    # Right up corner
                    RightUp = self.line_intersection(self.UpLine, self.RightLine)

                return LeftUp, LeftDown, RightDown, RightUp
            except NameError:
                print("FieldDetection.detect_field: error occurred")
                # self.Gamma_Min = self.Gamma_Min + 1
                # if (self.Gamma_Min > 255): self.Gamma_Min = 0

            # try:
            #     if self.UpLine and self.LeftLine:
            #         # Left up corner
            #         LeftUp = self.line_intersection(self.UpLine[0], self.LeftLine[0])
            #     if self.DownLine and self.LeftLine:
            #         # Left down corner
            #         LeftDown = self.line_intersection(self.DownLine[0], self.LeftLine[0])
            #     if self.DownLine and self.RightLine:
            #         # Right down corner
            #         RightDown = self.line_intersection(self.DownLine[0], self.RightLine[0])
            #     if self.UpLine and self.RightLine:
            #         # Right up corner
            #         RightUp = self.line_intersection(self.UpLine[0], self.RightLine[0])
            #
            #     return LeftUp, LeftDown, RightDown, RightUp
            #
            # except NameError:
            #     self.Gamma_Min = self.Gamma_Min + 1
            #     if(self.Gamma_Min > 255) : self.Gamma_Min = 0

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
                 #raise Exception('lines do not intersect')
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

    def LinesFilter(self, slopeLines, threshold1, threshold2):

        # Net filter
        if threshold1 == LN and threshold2 == RN:
            slopeLines = slopeLines[slopeLines[..., 4] > 5]  # slope
        if slopeLines is not None:
            slopeLines = slopeLines[slopeLines[..., 0] > threshold1]  # x1
        if slopeLines is not None:
            slopeLines = slopeLines[slopeLines[..., 0] < threshold2]  # x1
        if slopeLines is not None:
            slopeLines = slopeLines[slopeLines[..., 2] > threshold1]  # x2
        if slopeLines is not None:
            slopeLines = slopeLines[slopeLines[..., 2] < threshold2]  # x2

        if len(slopeLines) >= 1:
            X1 = np.mean(slopeLines[..., 0])  # x1
            X2 = np.mean(slopeLines[..., 2])  # y1
            Y1 = np.mean(slopeLines[..., 1])  # x2
            Y2 = np.mean(slopeLines[..., 3])  # y2
            avgLine = int(X1), int(Y1), int(X2), int(Y2)
            return avgLine

    def draw_field(self, frame, Leftup, LeftDown, RightDown, RightUp):
        # Polygon corner points coordinates
        pts = np.array([Leftup, LeftDown, RightDown, RightUp])
        overlay = frame.copy()
        cv2.drawContours(overlay, [pts], 0, (255, 0, 255), -1)
        cv2.addWeighted(overlay, 0.2, frame, 1, 0, frame)
        return frame
        # FieldContour = np.array([Leftup, LeftDown, RightDown, RightUp])
        # FieldContour = FieldContour.reshape((-1, 1, 2))
        # cv2.polylines(frame, [FieldContour], True, (0, 0, 255), 2)
        # overlay = frame.copy()
        # # cv2.drawContours(overlay, [FieldContour], 0, (255, 0, 255), -1)
        # cv2.addWeighted(overlay, 0.2, frame, 1, 0, frame)
       # return frame