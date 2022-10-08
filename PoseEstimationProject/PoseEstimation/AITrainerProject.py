import cv2
import numpy as np
import time
import PoseModule as pm


cap = cv2.VideoCapture("PoseVideos/dumble.mp4")
#cap = cv2.VideoCapture(0)
pTime = 0
r1, r2 = 110, 170
detector = pm.poseDetector()
count = 0
dir = 0

while True:
    success, img = cap.read()
   # img = cv2.imread('PoseVideos/test.png')
    img = detector.findPose(img)
    lmList = detector.getPosition(img, draw=False)
    if len(lmList) != 0:
        # the left arm
      detector.findAngle(img, 11, 13, 15)
        # right arm
      angle = int(detector.findAngle(img, 12, 14, 16))

      per = int(np.interp(angle, (r1, r2), (0,100)))
      print (per, angle)


      # check for dumble curl
      if per == 100:
          if dir ==0:
              count +=0.5
              dir  = 1
      if per == 0:
          if dir == 1:
              count +=0.5
              dir =  0
    cv2.putText(img, f'{count}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 5, (100, 255, 100), 4)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # show results in camera fram
    img = cv2.resize(img, (420, 360), interpolation = cv2.INTER_AREA)
    cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.imshow("Image", img)
    key = cv2.waitKey(10)
    if key == 113:  # that is equivalent to 'q' character you can use any key i.e enter or space
        break

cap.release()
cv2.destroyAllWindows()

