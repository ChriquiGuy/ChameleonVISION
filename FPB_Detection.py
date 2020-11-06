import cv2
from  utils.motion_detection import MotionDetector

#!##########################!#
##! Must to have arguments !##

# Insert video full path
video_path = './videos/DJI_0825_Trim.mp4'
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



def main() :
    
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

    # Run over video
    while(cap.isOpened()):

        # Find object in motion and draw it in result frame
        motion_boxes = m_detection.find_motion_rects(current_frame, previous_frame, m_detection_frame)

        # Show frames
        cv2.imshow('Motion Detection', m_detection_frame)

        # Get next frame
        previous_frame = current_frame.copy()
        _, original_frame = cap.read()

        # Resize frame
        current_frame = cv2.resize(original_frame, dim, interpolation = cv2.INTER_AREA)

        # Refresh result frames to current frames
        result_frame = current_frame.copy()
        m_detection_frame = result_frame.copy()

        # Check if user press exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release capture
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
