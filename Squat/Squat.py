import cv2
from cvzone.PoseModule import PoseDetector as pd

cap = cv2.VideoCapture(0)
detector = pd() # 포즈 디텍터 객체 생성

flag = 0
count = 0

while cap.isOpened : # 카메라가 연결되었을 경우
    ret, img = cap.read() # 카메라로부터 이미지를 읽어옴
    img = cv2.flip(img, 1) # 영상 반전시키기
    img = detector.findPose(img) # 포즈 찾기

    lmlist, bbox = detector.findPosition(img, draw= True) # 포즈의 위치 찾기
    # 11, 13, 15 오른팔
    # 12, 14, 16 왼팔

    if lmlist :
        left_color = (0, 0, 255)  # 기본 색상 (빨강)
        right_color = (0, 0, 255)  # 기본 색상 (빨강)

        rightA, img = detector.findAngle(lmlist[11], lmlist[13], lmlist[15], img=img, color=right_color, scale=10)
        leftA, img = detector.findAngle(lmlist[12], lmlist[14], lmlist[16], img=img, color=left_color, scale=10)

        if leftA >= 270:
           left_color = (0, 255, 0)  # 각도가 120 이하일 때 색상 (초록)
        
        if rightA <= 120:
           right_color = (0, 255, 0)  # 각도가 120 이하일 때 색상 (초록)

        rightA, img = detector.findAngle(lmlist[11], lmlist[13], lmlist[15], img=img, color=right_color, scale=10)
        leftA, img = detector.findAngle(lmlist[12], lmlist[14], lmlist[16], img=img, color=left_color, scale=10)
        
        if leftA > 270 and rightA < 90 and flag == 0:
            count = count + 1
            flag = 1
        elif leftA < 210 and rightA > 150 and flag == 1:
            flag = 0

    cv2.putText(img, text = "Squat count : " + str(count), org = (10, 30), 
        fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
        fontScale=1, 
        color=(0,0,255), 
        thickness = 2)

    if ret :
            cv2.imshow('view', img) # 이미지를 화면에 출력

    if cv2.waitKey(1) == ord('q') : # q를 누르면 종료
        break
