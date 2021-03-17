import cv2
import time

CONFIDENCE_THRESHOLD = 0.1
NMS_THRESHOLD = 0.1
COLORS = [(255, 100, 100), (255, 255, 0)]


class ObjectDetection():

    class_names = []
    model = None


    def initialize_model(self):

        with open("./model/volley.names", "r") as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

        net = cv2.dnn.readNet("./model/volley.weights", "./model/volley.cfg")
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(416, 416), scale=1/255)


    def detect(self, frame):
        self.classes, scores, boxes = self.model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        return self.classes, scores, boxes


    def draw_objects(self, frame, classes, scores, boxes):

        for (classid, score, box) in zip(classes, scores, boxes):
            color = COLORS[int(classid) % len(COLORS)]
            label = "(%d, %d)" % (get_box_center(box)[0], get_box_center(box)[1])
            overlay = frame.copy()
            cv2.rectangle(overlay, box, color, -1)
            cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
            cv2.putText(frame, label, (box[0] , box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
            

        return frame



def get_box_center(box):
    return (box[0] - box[2]/2, box[1]- box[3]/2)
