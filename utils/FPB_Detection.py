import cv2
import time

from  utils.motion_detection import MotionDetector
from utils.object_tracker import ObjectTracker
from utils.object_detection import ObjectDetection


#!##########################!#
##! Must to have arguments !##

# Insert video full path
video_path = './videos/12.mp4'
# Insert resize scale precents
resize_scale_percent = 50

##! Must to have arguments !##
#!##########################!#



def get_resize_dim(frame, scale_percent) : 

    # Resize parameters initialize
    width  = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    return dim



def remove_out_of_range_boxes(boxes):
    good_boxes = []

    for box in boxes:
        good = True
        for point in box:
            if point[1] > 350 or point[1] < 70 : good = False
        if good : good_boxes.append(box)

    return good_boxes




def main() :

    
    time_per_frame_CNN = 0
    time_per_frame_CV = 0
    avg_time_CV = 0
    avg_time_CNN = 0
    frame_count = 0
    
    # Get first frame
    cap = cv2.VideoCapture(video_path)
    _, original_frame = cap.read()

    # Get frame resize dim by scale precents
    dim = get_resize_dim(original_frame, resize_scale_percent)

    # Resize frame
    current_frame = cv2.resize(original_frame, dim, interpolation = cv2.INTER_AREA)

    # Init previous frame from current frame
    previous_frame = current_frame
    result_frame = current_frame

    # Init motion method
    m_detection = MotionDetector()
    m_detection_frame = result_frame
    motion_boxes = []

    # Init object detection method
    o_detection = ObjectDetection()
    o_detection.initialize_model()
    o_detection_frame = result_frame
    detection_boxes = []

    # Init tracker method
    # o_tracker = ObjectTracker()
    # o_tracker.initialize_model()
    # o_tracker_frame = result_frame
    # tracker_boxes = []

    # Run over video
    while(cap.isOpened()):

        frame_count += 1

        # Find object in motion and draw it in motion result frame
        start = time.time()
        motion_boxes = m_detection.find_motion_rects(current_frame, previous_frame, m_detection_frame)
        end = time.time()
        time_per_frame_CV += (end - start)
        avg_time_CV = time_per_frame_CV / frame_count
        
        # motion_boxes = remove_out_of_range_boxes(motion_boxes)

       
        # Find object in tracker and draw it in tracker result frame
        # detection_boxes = o_tracker.find_tracker_rects(current_frame, o_detection_frame)
        # Find object in detection and draw it in object detection result frame
        start = time.time()
        classes, scores, detection_boxes = o_detection.detect(current_frame)
        end = time.time()
        time_per_frame_CNN += (end - start)
        avg_time_CNN = time_per_frame_CNN / frame_count

        # Draw boxes on result frame
        cv2.drawContours(m_detection_frame, motion_boxes, -1, (0, 255, 0), 2)
        o_detection_frame = o_detection.draw_boxes(o_detection_frame, classes, scores, detection_boxes)

        # Show frames
        cv2.imshow('Motion Detection', m_detection_frame)
        cv2.imshow('CNN Object Detection', o_detection_frame)

        print("avg_time_CV = " +str(avg_time_CV * 1000).split('.')[0] + " (milliseconds)")
        print("avg_time_CNN = " +str(avg_time_CNN * 1000).split('.')[0] + " (milliseconds)")


        # Get next frame
        previous_frame = current_frame.copy()
        _, original_frame = cap.read()
        _, original_frame = cap.read()

        # Resize frame
        current_frame = cv2.resize(original_frame, dim, interpolation = cv2.INTER_AREA)

        # Refresh result frames to current frames
        result_frame = current_frame.copy()
        m_detection_frame = result_frame.copy()
        o_detection_frame = result_frame.copy()

        # Check if user press exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release capture
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
