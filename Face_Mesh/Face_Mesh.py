import cv2
from cvzone.FaceMeshModule import FaceMeshDetector as fmd

cap = cv2.VideoCapture(0)
detector = fmd(maxFaces=1, minDetectionCon=0.75)
count = 0

while cap.isOpened : # 카메라가 연결되었을 경우
    ret, img = cap.read() # 카메라로부터 이미지를 읽어옴
    if ret :

        img,face = detector.findFaceMesh(img, draw = True) # 얼굴을 찾는 함수 실행
        if face: # 얼굴이 인식되었을 경우

            img = cv2.flip(img, 1) # 영상 반전시키기

            leftEyeVDis, info = detector.findDistance(face[0][23], face[0][27]) # 왼쪽 눈의 수직 거리 구하기
            leftEyeHDis, info = detector.findDistance(face[0][130], face[0][243]) # 왼쪽 눈의 수평 거리 구하기
            ratio = leftEyeVDis/leftEyeHDis # 수직 거리를 수평 거리로 나누기
            print(ratio) # 왼쪽 눈의 수직 거리 출력
            
            if ratio < 0.6:
                cv2.putText(img, text = "Wake up!!!", org = (10, 30), 
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=1, 
                color=(0,0,255), 
                thickness = 2)

            cv2.imshow('view', img) # 이미지를 화면에 출력

    if cv2.waitKey(1) == ord('q') : # q를 누르면 종료
        break