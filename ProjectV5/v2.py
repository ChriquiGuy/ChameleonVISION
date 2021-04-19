import cv2
import numpy as np

# empty arrays
x = []
y = []
classes = []
font = cv2.FONT_HERSHEY_PLAIN

# Ball parameters
MState = True
Current_slope = 0
Previous_slope = 0
BallInOut = 0
BallCenter_Coordinates = []
event = ""
event_time = 0

# Field parameters
LeftUp = (351, 231)
LeftDown = (385, 869)
RightDown = (1629, 850)
RightUp = (1608, 231)
FieldContour = np.array([LeftUp, LeftDown, RightDown, RightUp])

WEIGHT_OF_SCREEN = 1274
HEIGHT_OF_SCREEN = 720

# Lines threshold
# Net Detection
NTL = WEIGHT_OF_SCREEN * 0.35
NTR = WEIGHT_OF_SCREEN * 0.65

# Left line
LTL = WEIGHT_OF_SCREEN * 0.1
LTR = WEIGHT_OF_SCREEN * 0.3

# Right line
RTL = WEIGHT_OF_SCREEN * 0.8
RTR = WEIGHT_OF_SCREEN * 0.95

# Up line
UTT = HEIGHT_OF_SCREEN * 0.1
DTT = HEIGHT_OF_SCREEN * 0.35

# Bottom Line
UTB = HEIGHT_OF_SCREEN * 0.7
DTB = HEIGHT_OF_SCREEN * 0.95


print(classes)

# Load RTMP
cap = cv2.VideoCapture('/home/chameleonvision/Desktop/Project/videos/videos_720p/DJI_0858_Trim.mp4')

# Video Writer
# out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 25, (1920, 1080))

# Load net
#net = cv2.dnn.readNet('volley.weights', 'volley.cfg')
net = cv2.dnn.readNet('/home/chameleonvision/Desktop/Project/model/volley.weights', '/home/chameleonvision/Desktop/Project/model/volley.cfg')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

with open('/home/chameleonvision/Desktop/Project/model/volley.names', 'r') as f:
    classes = f.read().splitlines()

# with open('volley.names', 'r') as f:
#     classes = f.read().splitlines()


def line_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    a1, b1, a2, b2 = line2

    # Line1
    S_pointLine1 = (x1, y1)
    E_pointLine1 = (x2, y2)

    # Line2
    S_pointLine2 = (a1, b1)
    E_pointLine2 = (a2, b2)

    xdiff = (x1 - x2, a1 - a2)
    ydiff = (y1 - y2, b1 - b2)

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(S_pointLine1, E_pointLine1), det(S_pointLine2, E_pointLine2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return int(x), int(y)

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def translate(value, leftMin, leftMax, rightMin, rightMax):
    try:
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return int(rightMin + (valueScaled * rightSpan))
    except NameError:
        print("can't divide by zero")

def SlopeCalc(lines):
    Angle_Sum = np.array([(180 / np.pi) * np.arctan2(lines[:, :, 3] - lines[:, :, 1],
                                                     lines[:, :, 2] - lines[:, :, 0])])
    Angle_Sum = Angle_Sum.reshape(Angle_Sum.shape[1], Angle_Sum.shape[0], Angle_Sum.shape[2])
    SlopeLines = np.append(lines, Angle_Sum, axis=2)
    return SlopeLines

def LinesFilter(SlopeLines):
    # Net filter
    NetLine = SlopeLines[SlopeLines[..., 4] > 5]  # x1
    if NetLine is not None:
        NetLine = NetLine[NetLine[..., 0] > NTL]          #x1
    if NetLine is not None:
        NetLine = NetLine[NetLine[..., 0] < NTR]      #x1
    if NetLine is not None:
        NetLine = NetLine[NetLine[..., 2] > NTL]      #x2
    if NetLine is not None:
        NetLine = NetLine[NetLine[..., 2] < NTR]      #x2

    if len(NetLine) > 1:
        X1 = np.mean(NetLine[..., 0])     # x1
        X2 = np.mean(NetLine[..., 2])     # y1
        Y1 = np.mean(NetLine[..., 1])     # x2
        Y2 = np.mean(NetLine[..., 3])     # y2

        cv2.line(current_frame, (int(X1), int(Y1)), (int(X2), int(Y2)), (0, 255, 0), 8, cv2.LINE_AA)
        NetLine = int(X1), int(Y1), int(X2), int(Y2)

    # Up line
    UpLine = SlopeLines[SlopeLines[..., 1] > UTT]           #y1
    if UpLine is not None:
        UpLine = UpLine[UpLine[..., 1] < DTT]       #y1
    if UpLine is not None:
        UpLine = UpLine[UpLine[..., 3] > UTT]       #y2
    if UpLine is not None:
        UpLine = UpLine[UpLine[..., 3] < DTT]       #y2

        if len(UpLine) > 1:
            X1 = np.mean(UpLine[..., 0])  # x1
            X2 = np.mean(UpLine[..., 2])  # y1
            Y1 = np.mean(UpLine[..., 1])  # x2
            Y2 = np.mean(UpLine[..., 3])  # y2

            cv2.line(current_frame, (int(X1), int(Y1)), (int(X2), int(Y2)), (0, 0, 255), 8, cv2.LINE_AA)

            UpLine = int(X1), int(Y1), int(X2), int(Y2)

    # Left line
    LeftLine = SlopeLines[SlopeLines[..., 0] > LTL]         # x1
    if LeftLine is not None:
        LeftLine = LeftLine[LeftLine[..., 0] < LTR]     # x1
    if LeftLine is not None:
        LeftLine = LeftLine[LeftLine[..., 2] > LTL]     # x2
    if LeftLine is not None:
        LeftLine = LeftLine[LeftLine[..., 2] < LTR]     # x2

        if len(LeftLine) > 1:
            X1 = np.mean(LeftLine[..., 0])  # x1
            X2 = np.mean(LeftLine[..., 2])  # y1
            Y1 = np.mean(LeftLine[..., 1])  # x2
            Y2 = np.mean(LeftLine[..., 3])  # y2

            cv2.line(current_frame, (int(X1), int(Y1)), (int(X2), int(Y2)), (255,0 , 0), 8, cv2.LINE_AA)

            LeftLine = int(X1), int(Y1), int(X2), int(Y2)

    # Down line
    DownLine = SlopeLines[SlopeLines[..., 1] > UTB]         # y1
    if DownLine is not None:
        DownLine = DownLine[DownLine[..., 1] < DTB]     # y1
    if DownLine is not None:
        DownLine = DownLine[DownLine[..., 3] > UTB]     # y2
    if DownLine is not None:
        DownLine = DownLine[DownLine[..., 3] < DTB]     # y2

        if len(DownLine) > 1:
            X1 = np.mean(DownLine[..., 0])  # x1
            X2 = np.mean(DownLine[..., 2])  # y1
            Y1 = np.mean(DownLine[..., 1])  # x2
            Y2 = np.mean(DownLine[..., 3])  # y2

            cv2.line(current_frame, (int(X1), int(Y1)), (int(X2), int(Y2)), (255, 255, 0), 8, cv2.LINE_AA)

            DownLine = int(X1), int(Y1), int(X2), int(Y2)

    # Right line
    RightLine = SlopeLines[SlopeLines[..., 0] > RTL]        # x1
    if RightLine is not None:
        RightLine = RightLine[RightLine[..., 0] < RTR]    # x1
    if RightLine is not None:
        RightLine = RightLine[RightLine[..., 2] > RTL]    # x2
    if RightLine is not None:
        RightLine = RightLine[RightLine[..., 2] < RTR]    # x2

        if len(RightLine) > 1:
            X1 = np.mean(RightLine[..., 0])  # x1
            X2 = np.mean(RightLine[..., 2])  # y1
            Y1 = np.mean(RightLine[..., 1])  # x2
            Y2 = np.mean(RightLine[..., 3])  # y2

            cv2.line(current_frame, (int(X1), int(Y1)), (int(X2), int(Y2)), (0, 255, 255), 8, cv2.LINE_AA)

            RightLine = int(X1), int(Y1), int(X2), int(Y2)

    return NetLine, UpLine, LeftLine, DownLine, RightLine

def empty(a):
    pass


# cv2 bars
cv2.namedWindow("GammaBars")
cv2.resizeWindow("GammaBars", 640, 80)
cv2.createTrackbar("Gamma Min", "GammaBars", 0, 255, empty)
cv2.createTrackbar("Gamma Max", "GammaBars", 255, 255, empty)

# Get width and height of video stream
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while cap.isOpened():

    # Line classification
    UpLine = []
    LeftLine = []
    DownLine = []
    RightLine = []
    NetLine = []

    # Field area
    x = []
    y = []

    m = 0
    ret, current_frame = cap.read()

    if ret:

        current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)  # Gray
        current_frame_copy = current_frame.copy()

        Gamma_Min = cv2.getTrackbarPos("Gamma Min", "GammaBars")
        Gamma_Max = cv2.getTrackbarPos("Gamma Max", "GammaBars")

        res, binary = cv2.threshold(current_frame_gray, Gamma_Min, Gamma_Max, cv2.THRESH_BINARY)  # Threshold
        edges = cv2.Canny(binary, 1, 255)  # Canny algorithm

        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 7, np.array([]), 200, 100)  # HoughLinesP

        if lines is not None:
            SlopeLines = SlopeCalc(lines)
            NetLine, UpLine, LeftLine, DownLine, RightLine = LinesFilter(SlopeLines)

            try:
                if len(UpLine) == 4 and len(LeftLine) == 4:
                    # Left up corner
                    LeftUp = line_intersection(UpLine, LeftLine)

                if len(DownLine) == 4 and len(LeftLine) == 4:
                    # Left down corner
                    LeftDown = line_intersection(DownLine, LeftLine)

                if len(DownLine) == 4 and len(RightLine) == 4:
                    # Right down corner
                    RightDown = line_intersection(DownLine, RightLine)

                if len(UpLine) == 4 and len(RightLine) == 4:
                    # Right up corner
                    RightUp = line_intersection(UpLine, RightLine)
            except NameError:
                print("No 4 lines found")

        # Print simulation -> field
        try:
            cv2.putText(current_frame, " Field Area", (850, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
            cv2.rectangle(current_frame, (850, 55), (1070, 110), (0, 0, 255), 2)
            cv2.line(current_frame, (960, 45), (960, 120), (255, 0, 0), 2)
            # field area
            if y and x is not None:
                cv2.putText(current_frame, str(LeftUp), (700, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (255, 0, 0), 2)
                cv2.putText(current_frame, str(RightDown), (1100, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (255, 0, 0), 2)
                cv2.putText(current_frame, str(RightUp), (1100, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (255, 0, 0), 2)
                cv2.putText(current_frame, str(LeftDown), (700, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (255, 0, 0), 2)
        except NameError:
            print("ValueError: min() arg is an empty sequence")

        try:
            # Polygon corner points coordinates
            FieldContour = np.array([LeftUp, LeftDown, RightDown, RightUp])
            FieldContour = FieldContour.reshape((-1, 1, 2))
            isClosed = True
            cv2.polylines(current_frame_copy, [FieldContour], isClosed, (255, 0, 0), 2)
        except NameError:
            print("No 4 lines found")

        #   Darknet detect
        blob = cv2.dnn.blobFromImage(current_frame_copy, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        layerOutputs = net.forward(output_layers_names)

        boxes = []
        confidences = []
        class_ids = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i], 2))

                if label == 'Ball':

                    BallCenter = (x + int(w / 2), y + int(h / 2))
                    BallCenter_Coordinates.append(BallCenter)

                    if len(BallCenter_Coordinates) > 3:

                        ball_y2 = BallCenter_Coordinates[-1][1]
                        ball_y1 = BallCenter_Coordinates[-2][1]
                        ball_x2 = BallCenter_Coordinates[-1][0]
                        ball_x1 = BallCenter_Coordinates[-2][0]

                        if (ball_x2 - ball_x1) != 0:

                            m = int((ball_y2 - ball_y1) / (ball_x2 - ball_x1))
                            cv2.putText(current_frame_copy, "Slope:" + " " + str(m), (x, y + 150),
                                        font, 2, (0, 0, 170), 2)
                            cv2.line(current_frame_copy, BallCenter_Coordinates[-3], BallCenter_Coordinates[-1],
                                     (0, 0, 170), 5)

                            # Ball In / Ball Out
                            MState = not MState
                            if MState is True:
                                Current_slope = int((ball_y2 - ball_y1) / (ball_x2 - ball_x1))
                            elif MState is False:
                                Previous_slope = int((ball_y2 - ball_y1) / (ball_x2 - ball_x1))

                            # Change direction
                            if Current_slope != Previous_slope:
                                BallInOut = int(cv2.pointPolygonTest(FieldContour, BallCenter, True))

                                #   Ball In
                                if BallInOut >= 0:
                                    cv2.putText(current_frame_copy, "Ball In", (1300, 100),
                                                font, 3, (0, 255, 0), 2)
                                    event = "In"
                                    event_time = cap.get(cv2.CAP_PROP_POS_MSEC)
                                else:
                                    # Ball Out
                                    cv2.putText(current_frame_copy, "Ball Out :" + str(abs(BallInOut)) + "cm",
                                                (1300, 100), font, 3, (0, 0, 170), 2)
                                    event = "Out"
                                    event_time = cap.get(cv2.CAP_PROP_POS_MSEC)


                    # Print simulation -> Ball
                    try:
                        BallCenter_X = translate(BallCenter[0], int((LeftUp[0]+LeftDown[0])/2),
                                                 int((RightUp[0]+RightDown[0])/2), 850, 1070)
                        BallCenter_Y = translate(BallCenter[1], int((LeftUp[1] + RightUp[1])/2),
                                                 int((LeftDown[1] + RightDown[1])/2), 55, 110)
                        cv2.circle(current_frame, (BallCenter_X, BallCenter_Y), 5, (0, 0, 255), -1)
                    except NameError:
                        print("No ball detect")


                    current_time = cap.get(cv2.CAP_PROP_POS_MSEC)

                    if current_time <= event_time + 2000:
                        if event == "In":
                            cv2.putText(current_frame_copy, "Ball In", (750, 100), font, 3, (0, 255, 0), 2)
                        elif event == "Out":
                            cv2.putText(current_frame_copy, "Ball Out :" + str(abs(BallInOut)) + "cm", (750, 100),
                                        font, 3, (0, 0, 170), 2)

                    # Ball
                    cv2.circle(current_frame_copy, BallCenter, int(w / 2), (0, 0, 255), 2)
                    # cv2.rectangle(current_frame_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(current_frame_copy, label + " " + confidence, (x, y + 100), font, 2, (0, 0, 170), 2)
                else:
                    # Player
                    # Player
                    cv2.rectangle(current_frame_copy, (x, y), (x + w, y + h), (0, 0, 0), 2)
                    cv2.putText(current_frame_copy, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)

        imgStack = stackImages(0.5, ([current_frame, current_frame_copy], [binary, edges]))

        # Video Write
        # out.write(imgStack)

        cv2.imshow('sourceImg', imgStack)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(BallCenter_Coordinates)
            break

        # Show current position in milliseconds
        if cv2.waitKey(1) & 0xFF == ord('s'):
            print("Position : %d" % cap.get(cv2.CAP_PROP_POS_MSEC))

        # Move VIDEO 2 seconds
        if cv2.waitKey(1) & 0xFF == ord('m'):
            cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) + 2000)
        if cv2.waitKey(1) & 0xFF == ord('n'):
            cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) + 2000)

    else:
        print("RTMP IS NOT CONNECTED")

cap.release()

# Video Write
# out.release()

# Closes all the frames
cv2.destroyAllWindows()