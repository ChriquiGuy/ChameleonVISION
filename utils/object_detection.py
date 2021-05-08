import cv2
from .helper import *
import time

CONFIDENCE_THRESHOLD = 0.6
NMS_THRESHOLD = 0.1
COLORS = [(0, 100, 255) , (100, 255, 255), (255, 255, 0)]


class ObjectDetection():

    class_names = []
    model = None

    def initialize_model(self):

        with open("/home/chameleonvision/Desktop/Project/model/volley.names", "r") as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

        net = cv2.dnn.readNet("/home/chameleonvision/Desktop/Project/model/volley.weights", "/home/chameleonvision/Desktop/Project/model/volley.cfg")
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)


    def detect(self, frame):
        self.classes, scores, boxes = self.model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        return self.classes, scores, boxes


    def draw_objects(self, frame, classes, scores, boxes, field_center):

        for (classid, score, box) in zip(classes, scores, boxes):
            
            color = COLORS[2]
            if(classid[0] == 0) :
                if(get_box_center(box)[0] < field_center) : color = COLORS[0]
                else : color = COLORS[1]
                
            # color = COLORS[int(classid) % len(COLORS)]
            label = "(%d, %d)" % (get_box_center(box)[0], get_box_center(box)[1])
            overlay = frame.copy()
            cv2.rectangle(overlay, box, color, -1)
            cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
            cv2.putText(frame, label, (box[0] , box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
            
        return frame

