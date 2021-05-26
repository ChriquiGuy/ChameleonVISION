import cv2
from .helper import *

CONFIDENCE_THRESHOLD = 0.65
NMS_THRESHOLD = 0.1
COLORS = [(255, 0, 0), (0, 0, 255), (195, 195, 195), (0, 255, 0)]


class ObjectDetection:
    class_names = []
    model = None

    ball_flag = True
    current_ball = None
    prev_ball = None

    def initialize_model(self):

        with open('./model/volley.names', 'r') as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

        net = cv2.dnn.readNet('/home/chameleonvision/Desktop/FinalProject/ChameleonVISION/model/volley.weights',
                              './model/volley.cfg')

        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

    def detect(self, frame):
        self.classes, scores, boxes = self.model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        return self.classes, scores, boxes

    def draw_tracking(self, result_frame, objects_bbs_ids, ball_box):

        if objects_bbs_ids is not None:
            for object in objects_bbs_ids:
                x, y, w, h, index = object
                # cv2.rectangle(result_frame, (x, y), (x + w, y + h), (200, 200, 200), 1)
                # cv2.putText(result_frame, str(index), (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        return result_frame

    def draw_objects(self, frame, classes, scores, boxes, field_center, LeftUp, LeftDown, RightDown, RightUp):

        for (classid, score, box) in zip(classes, scores, boxes):

            color = COLORS[2]
            if classid[0] == 0:

                # Check if player inside the field
                playerContour = np.array([LeftUp, LeftDown, RightDown, RightUp])
                playerContour.reshape((-1, 1, 2))
                player_inside_field = int(cv2.pointPolygonTest(playerContour, get_box_center(box), True))
                if player_inside_field >= 0:
                    # Left side
                    if field_center and get_box_center(box)[0] < field_center:
                        color = COLORS[0]
                    # Right side
                    else:
                        color = COLORS[1]

            label = "(%d, %d)" % (get_box_center(box)[0], get_box_center(box)[1])
            overlay = frame.copy()

            # Draw player
            if classid[0] == 0:
                cv2.rectangle(overlay, box, color, -1)
                cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
                cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            # Draw ball
            if classid[0] == 1:
                ballMidpoint = (get_box_center(box)[0], get_box_center(box)[1])
                # self.ball_flag = not self.ball_flag
                # if self.ball_flag:
                #     self.current_ball = ballMidpoint
                # else:
                #     self.prev_ball = ballMidpoint
                # try:
                #     cv2.line(overlay, self.current_ball, self.prev_ball, (0, 0, 255), 4, cv2.LINE_AA)
                # except NameError:
                #     print("cannot print ball line")

                cv2.circle(overlay, ballMidpoint, int(box[2] / 2), COLORS[3], 2)
                cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
                cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        return frame

    def switch_sides(self):
        color_0 = COLORS[0]
        color_1 = COLORS[1]
        COLORS[1] = color_0
        COLORS[0] = color_1
