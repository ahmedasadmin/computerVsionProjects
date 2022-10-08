import cv2
import mediapipe as mp
import time



cap = cv2.VideoCapture(0) # video camp number 0 -- you can use num 1


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
   # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
           for id, lm in enumerate(handLms.landmark):
               #print(id,lm)
               h, w, c =img.shape
               cx, cy = int(lm.x*w), int(lm.y*h)
               print(id, cx, cy)
              #if id == 20:
               cv2.circle(img, (cx, cy), 20, (200, 100, 50), cv2.FILLED)


           mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime- pTime)
    pTime = cTime


    cv2.putText(img, str(int(fps)), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 113 :# that is equivalent to 'q' character you can use any key i.e enter or space
        break
cap.release()
cv2.destroyAllWindows()


