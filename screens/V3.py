import cv2
import numpy as np


WEIGHT_OF_SCREEN = 1920
HEIGHT_OF_SCREEN = 1080
LTL = 250
LTR = 750
RTL = 1300
RTR = 1750


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

print(classes)

# Load RTMP
# cap = cv2.VideoCapture('rtmp://127.0.0.1:1935/ChameleonVISION/1234')          # checkRTMP server.txt
cap = cv2.VideoCapture('/home/chameleonvision/Desktop/Project/videos/858.MP4')  # 843, 827, 843, 858full

# Video Writer
# out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 25, (1920, 1080))

# Load net
# net = cv2.dnn.readNet('volley.weights', 'volley.cfg')
net = cv2.dnn.readNet('/home/chameleonvision/Desktop/Project/model/volley.weights', '/home/chameleonvision/Desktop/Project/model/volley.cfg')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

with open('/home/chameleonvision/Desktop/Project/model/volley.names', 'r') as f:
    classes = f.read().splitlines()


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

def filterLines(linesP):
    # Draw my lines
    NetLine = linesP[linesP[..., 0] > LTR]
    NetLine = NetLine[NetLine[..., 0] < RTL]

    # if (LTR < x1 < RTL) & (LTR < x2 < RTL):
    #             NetLine.append(linesP[i][0])
    #             slope = (y2 - y1) / (x2 - x1)
    #             if slope > 5:
    #                 cv2.line(current_frame, (x1, y1), (x2, y2), (255, 0, 0), 2, cv2.LINE_AA)
    #         # Up line
    #         elif (0 < y1 < 400) & (0 < y2 < 400):
    #             UpLine.append(linesP[i][0])
    #             cv2.line(current_frame, (x1, y1), (x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
    #         # Left line
    #         elif (0 < x1 < 500) & (0 < x2 < 500):
    #             LeftLine.append(linesP[i][0])
    #             cv2.line(current_frame, (x1, y1), (x2, y2), (0, 0, 255), 2, cv2.LINE_AA)
    #         # Down line
    #         elif (750 < y1 < 1000) & (750 < y2 < 1000):
    #             DownLine.append(linesP[i][0])
    #             cv2.line(current_frame, (x1, y1), (x2, y2), (255, 128, 0), 2, cv2.LINE_AA)
    #         # Right line
    #         elif (1500 < x1 < 1850) & (1500 < x2 < 1850):
    #             RightLine.append(linesP[i][0])
    #             cv2.line(current_frame, (x1, y1), (x2, y2), (255, 0, 255), 2, cv2.LINE_AA)

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

        linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 7, np.array([]), 500, 100)  # HoughLinesP

       #................ code from noteped enter here...................................

        if linesP is not None:
            x.append(x1)
                x.append(x2)
                if 250 < x1 < 650:
                    y.append(y1)
                if 1300 < x2 < 1750:
                    y.append(y2)

            try:
                cv2.putText(current_frame, " Field Area", (1600, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                cv2.rectangle(current_frame, (1600, 55), (1800, 150), (0, 0, 255), 2)
                # field area
                if y and x is not None:
                    cv2.putText(current_frame, str(min(x)), (1600, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.putText(current_frame, str(max(x)), (1745, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.putText(current_frame, str(min(y)), (1810, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.putText(current_frame, str(max(y)), (1810, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            except NameError:
                print("ValueError: min() arg is an empty sequence")

        try:
            if UpLine and LeftLine:
                # Left up corner
                LeftUp = line_intersection(UpLine[0], LeftLine[0])

            if DownLine and LeftLine:
                # Left down corner
                LeftDown = line_intersection(DownLine[0], LeftLine[0])

            if DownLine and RightLine:
                # Right down corner
                RightDown = line_intersection(DownLine[0], RightLine[0])

            if UpLine and RightLine:
                # Right up corner
                RightUp = line_intersection(UpLine[0], RightLine[0])
        except NameError:
            print("No 4 lines found")

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

        # classes, scores, detection_boxes = net.detect()
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

                    # Print
                    current_time = cap.get(cv2.CAP_PROP_POS_MSEC)

                    if current_time <= event_time + 2000:
                        if event == "In":
                            cv2.putText(current_frame_copy, "Ball In", (1300, 100), font, 3, (0, 255, 0), 2)
                        elif event == "Out":
                            cv2.putText(current_frame_copy, "Ball Out :" + str(abs(BallInOut)) + "cm", (1300, 100),
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



