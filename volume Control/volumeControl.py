import cv2
import mediapipe as mp
import numpy as np
import alsaaudio
mixer = alsaaudio.Mixer()





cap = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
x1 = 0
y1 = 0
y2 = 0
x2 = 0
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output  = my_hands.process(RGB)
    hands_landmark = output.multi_hand_landmarks

    if hands_landmark:
        for hand_landmark in hands_landmark:
            drawing_utils.draw_landmarks(frame, hand_landmark)
            landmarks = hand_landmark.landmark
            for id, landmark in enumerate(landmarks):

  
                if id == 8 :
                    x8, y8 = int(landmark.x *frame.shape[1]), int(landmark.y * frame.shape[0])
                    cv2.circle(img=frame, center=(x8,y8), radius=1, color=(255, 255, 255), thickness=2)
                    x1 = x8
                    y1 = y8
                    
                if id == 4 :
                    x4, y4 = int(landmark.x *frame.shape[1]), int(landmark.y * frame.shape[0])
                    cv2.circle(img=frame, center=(x4,y4), radius=1, color=(255, 255, 255), thickness=2)
                    x2 = x4
                    y2 = y4
                 
                cv2.line(frame, (x1, y1), (x2, y2), color=(255, 255, 255), thickness=2)
        a = np.array([x1, y1], dtype=np.float32)
        b = np.array([x2, y2], dtype=np.float32)
        dist = np.sqrt(np.sum(np.square(a- b) ) ) 
        dist =int (np.interp(dist, [20, 250], [0, 100]))
                # dist = dist/250
        print(dist)
        if (dist > 30):
            mixer.setvolume(dist)  # Set volume to 70%
        else:
            mixer.setvolume(10)
            
        
    # Display the frame
    cv2.imshow('hand Landmarks', frame)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
