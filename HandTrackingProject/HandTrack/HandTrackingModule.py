import cv2
import mediapipe as mp
import time



class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands= maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipsId = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
       # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:

                   self.mpDraw.draw_landmarks(img, handLms,
                                              self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw= True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
               # print(id,lm)
               h, w, c = img.shape
               cx, cy = int(lm.x * w), int(lm.y * h)
               #print(id, cx, cy)
               self.lmList.append([id, cx, cy])
               # if id == 20:
               if draw:            # draw is optionally
                  cv2.circle(img, (cx, cy), 10, (0, 0, 0), cv2.FILLED)

        return self.lmList

    def fingersUp(self):
        fingers = []
        # thumb issue
        if self.lmList[self.tipsId[0]][1] > self.lmList[self.tipsId[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if self.lmList[self.tipsId[id]][2] < self.lmList[self.tipsId[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)  # video camp number 0 -- you can use num 1
    detector = handDetector()  # without any param --- using default ---

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
        if key == 113 :# that is equivalent to 'q' character you can use any key i.e enter or space
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
   main()