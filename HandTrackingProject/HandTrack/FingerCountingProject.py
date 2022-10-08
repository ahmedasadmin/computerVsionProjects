import cv2
import time
import os
import HandTrackingModule as htm
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
folderPath = 'FingerImages'
myList = os.listdir(folderPath)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    image = cv2.resize(image, (200, 250), interpolation=cv2.INTER_AREA)
    overlayList.append(image)


pTime = 0
detector = htm.handDetector(detectionCon=.8)
tipsId = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)


    if len(lmList) != 0:
        fingers = []
        # thumb issue
        if lmList[tipsId[0]][1] < lmList[tipsId[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if lmList[tipsId[id]][2] < lmList[tipsId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

       # print(fingers)
        numFingers = fingers.count(1)
        print(numFingers)

        h, w, c = overlayList[numFingers - 1].shape


       # print("the value of i is : ", i)
        img[0:h, 0:w] = overlayList[numFingers-1]
        cv2.rectangle(img, (20, 250), (170, 425), (40,200, 200), cv2.FILLED)
        cv2.putText(img, str(numFingers), (45, 375), cv2.FONT_HERSHEY_DUPLEX, 5, (100, 0, 250), 30)



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (640-30, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("camera", img)


    key = cv2.waitKey(1)
    if key == 113:
        break




cap.release()
cv2.destroyAllWindows()