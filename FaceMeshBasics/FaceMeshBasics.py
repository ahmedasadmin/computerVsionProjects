import cv2
import mediapipe as mp
import time

mpFaceMesh = mp.solutions.face_mesh
FaceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)


cap = cv2.VideoCapture(0)
pTime = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = FaceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS,
                                 drawSpec,drawSpec)
            for id,lm in enumerate(faceLms.landmark):
                h, w, c = img.shape
                x, y = int(lm.x*w), int(lm.y*h)




    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,250,0), 2)



    cv2.imshow("Video", img)
    key = cv2.waitKey(10)
    if key == 113:         # q charac
        break


cap.release()
cv2.destroyAllWindows()