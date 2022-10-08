import cv2
import mediapipe as mp
import time

class FaceMeshDetector():
    def __init__(self, staticMode=False,  maxFaces=1, minDetectionCon=0.5,minTrackingCon=0.5):
        self.staticMode = staticMode
        self.maxFaces   = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackingCon = minTrackingCon


        self.mpFaceMesh = mp.solutions.face_mesh
        self.FaceMesh = self.mpFaceMesh.FaceMesh(self.staticMode,self.maxFaces,
                                                 self.minDetectionCon,self.minTrackingCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)

    def findFaceMesh(self,img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.FaceMesh.process(imgRGB)
        if results.multi_face_landmarks:
            faces = []
            for faceLms in results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACE_CONNECTIONS, self.drawSpec, self.drawSpec)

                face =[]
                for id, lm in enumerate(faceLms.landmark):
                    h, w, c = img.shape
                    x, y = int(lm.x * w), int(lm.y * h)
                    cv2.putText(img, str(int(id)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, .2, (0, 250, 0), 1)

                    face.append([x,y])
                faces.append(face)
        return img, faces

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceMeshDetector()
    while True:
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img)


        if len(faces) != 0:
            print(len(faces))
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 250, 0), 2)

        cv2.imshow("Video", img)
        key = cv2.waitKey(10)
        if key == 113:  # q charac
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
   main()