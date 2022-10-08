import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
####################################################
# ahmed mohamed abdelgaber
# ai virtual board
# 2/18/2022
###################################################

folder = "canva"
myList = os.listdir(folder)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folder}/{imPath}')
    overlayList.append(image)



header = overlayList[0]
# print(header.shape)
cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 600)
imgCanvas = np.ones((480, 848, 3), np.uint8)
imgCanvas = imgCanvas * 255
pTime = 0
drawColor = (0, 255, 255)

detector = htm.handDetector(detectionCon=0.7, trackCon=.5)
xp, yp = 0, 0
radius = 5
brushThickness = 15
while True:
    ret, img  = cap.read()
    img = cv2.flip(img, 1)

    #2. find handlandmarks
    img = detector.findHands(img)
    lmlist  = detector.findPosition(img, draw=False)


    if len(lmlist) != 0:

        # tip of index and midle finger
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        #3. check whish fingers are up
        fingers = detector.fingersUp()
        #print(fingers)

    #4. if selection mode - Two fingers are up
        if fingers[1] and fingers[2]:
           # print("selection mode")
            cv2.circle(img, (x1, y1), 10, (255, 255, 0), cv2.FILLED)
            if y1 < 56:
                if 100<x1<200:
                    header = overlayList[0]
                    drawColor = (0, 255, 255)
                elif 200 < x1 < 400:
                    header = overlayList[1]
                    drawColor = (255, 255, 0)
                    radius = 5
                    brushThickness = 15
                elif 400 < x1 < 600:
                    header = overlayList[2]
                    drawColor = (0, 0, 0)
                    radius = 5
                    brushThickness = 15
                elif 600 < x1 < 800:
                    header = overlayList[3]
                    drawColor = (255, 255, 255)
                    radius = 20
                    brushThickness = 30

    #5. if drawing mode  - Index finger is up


        if fingers[1] and fingers[2] == False:
            #print("Drawing Mode")
            cv2.circle(img, (x1, y1), radius, drawColor, cv2.FILLED)
            if xp==0 and yp==0:
                xp, yp =x1, y1

                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                # cv2.circle(img, (x1, y1), radius, drawColor, cv2.FILLED)
                # cv2.circle(imgCanvas, (x1, y1), radius, drawColor, cv2.FILLED)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1
        if fingers.count(1) == 0:
            xp, yp = 0, 0



    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_or(img, imgInv)
    img = cv2.bitwise_and(img, imgCanvas)
    #seting our header image
    header = cv2.resize(header, (848, 56), interpolation=cv2.INTER_AREA)
    img[0:56, 0:848] = header
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.7, 0)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (20,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 2)
   # print(img.shape)
    cv2.imshow("cam", img)
    cv2.imshow("painter", imgCanvas)
    key = cv2.waitKey(1)
    if key == 113:
        break

cap.release()
cv2.destroyAllWindows()