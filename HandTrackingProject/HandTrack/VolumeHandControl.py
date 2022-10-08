import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
############################################################
wCam, hCam = 640,480
############################################################

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
vol = 0
volBar = 400
volPer = 0
detector = htm.handDetector(detectionCon=.7,trackCon= 0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange= volume.GetVolumeRange()         #range volume is (min= -65.25 - max= 0.0)

minVol = volRange[0]
maxVol= volRange[1]
while True:
    success, img = cap.read()
    #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    if len(lmList )!= 0:
        #value num 4 & value 8
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img,(x1, y1),15, (255, 0, 0),cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0),cv2.FILLED)
        cv2.line(img,(x1, y1), (x2, y2), (255, 0, 0),1)


        length = math.hypot(x2-x1, y2-y1) #maxlen = 238.4722206044134 & minlen = 25.01999200639361
        #print(length)
        # Hand range 50 - 220
        # Volume range -65 - 0
        vol = np.interp(length,[50, 200], [minVol, maxVol])
        volBar = np.interp(length, [50, 200], [400, 150])
        volPer = np.interp(length, [50, 200], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        #print(vol)
        if length < 50:
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (0,255,0),3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0,255,0),cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 2)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow("CAM", img)
    key = cv2.waitKey(1)
    if key == 113:
        break


cap.release()
cv2.destroyAllWindows()