import cv2
import mediapipe as mp
import time

#import HandTrackingModule

import HandTrackingModule as htm



pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)  # video camp number 0 -- you can use num 1
detector = htm.handDetector()  # without any param --- using default ---

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    list = detector.findPosition(img)
    if len(list) !=0:
        print(list[20])
    # print(list)
    # cal fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # show results in camera fram
    cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 113  :# that is equivalent to 'q' character you can use any key i.e enter or space
        break

cap.release()
cv2.destroyAllWindows()
