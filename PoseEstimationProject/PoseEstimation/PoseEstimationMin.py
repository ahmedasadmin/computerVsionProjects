import cv2
import mediapipe as mp
import time
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose  = mpPose.Pose()
cap = cv2.VideoCapture('PoseVideos/1.mp4')

# cap = cv2.VideoCapture(0)


pTime = 0
cTime = 0
while True:

    success,img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)


    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx, cy), 10, (255, 255, 0))


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

