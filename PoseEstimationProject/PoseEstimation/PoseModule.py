import cv2
import mediapipe as mp
import time
import math
class poseDetector():
    def __init__(self, mode= False, upBody= False, smooth= True,
                 detectionCon= 0.5, trackingCon= 0.5):
        self.mode = mode
        self.upBody    = upBody
        self.smooth  = smooth
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon
        self.posList = []

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose  = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon,
                                      self.trackingCon)

    def findPose(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)


        if self.results.pose_landmarks:
            if draw:
               self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
    def getPosition(self, img, draw=True):
        self.posList= []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.posList.append([id, cx, cy])
                if draw:
                   cv2.circle(img, (cx, cy), 10, (255, 255, 0))
        return self.posList

    def findAngle(self, img, p1, p2, p3, draw= True):
        # get the landmarks
        x1, y1 = self.posList[p1][1:]
        x2, y2 = self.posList[p2][1:]
        x3, y3 = self.posList[p3][1:]
        # get the angle , ya angle
        angle =math.degrees(math.atan2(y3-y2, x3-x2)- math.atan2(y1-y2, x1-x2))
        if angle < 0:
            angle = -angle
        if angle > 180:
            angle = 360 - angle



        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 15, (255, 255, 0))
            cv2.circle(img, (x1, y1), 10, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 255, 0))
            cv2.circle(img, (x2, y2), 10, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (255, 255, 0))
            cv2.circle(img, (x3, y3), 10, (255, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(angle)), (x2-20, y2+50),
                        cv2.FONT_HERSHEY_SIMPLEX,.5, (255, 0, 255), 2)
        return angle

def main():
    cap = cv2.VideoCapture('PoseVideos/1.mp4')

    # cap = cv2.VideoCapture(0)
    pdetector = poseDetector()

    pTime = 0
    cTime = 0
    while True:
        success, img = cap.read()

        img = pdetector.findPose(img)
        posList=  pdetector.getPosition(img, draw=True)

        if len(posList)!=0:
            print(posList[0])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        # show results in camera fram
        img = cv2.resize(img, (420, 360), interpolation = cv2.INTER_AREA)
        cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 113:  # that is equivalent to 'q' character you can use any key i.e enter or space
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()