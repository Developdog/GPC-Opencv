"""
python 3.10.0
pip install opencv-python
pip install mediapipe
pip install cvzone # 해당 라이브러리 3.12에서 사용 불가능, tensorflow 설치 시 오류 발생

"""

import cv2
from cvzone.HandTrackingModule import HandDetector
# import time

### 오디오 관련 라이브러리 추가

from ctypes import cast,POINTER # ctypes 모듈에서 cast, POINTER 함수를 가져옴
from comtypes import CLSCTX_ALL # comtypes 모듈에서 CLSCTX_ALL 함수를 가져옴
from pycaw.pycaw import AudioUtilities ,IAudioEndpointVolume # pycaw.pycaw 모듈에서 AudioUtilities, IAudioEndpointVolume 함수를 가져옴
devices=AudioUtilities.GetSpeakers() # 오디오 장치 정보를 가져옴
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None) # 오디오 장치 정보를 활성화
volume=cast(interface,POINTER(IAudioEndpointVolume)) # 오디오 장치 정보를 포인터로 변환

###


cap = cv2.VideoCapture(0) # # 열린 웹캠의 정보 값을 cap에 전달
detector = HandDetector(maxHands = 1, detectionCon = 0.75) # 손을 찾는 객체 생성
while cap.isOpened : # 카메라가 연결되었을 경우
    ret, img = cap.read() # 카메라로부터 이미지를 읽어옴
    if ret :

        img = cv2.flip(img, 1) # 영상 반전시키기
        hands, img = detector.findHands(img, flipType = False) # 영상에서 손 감지시키기
        if len(hands) >= 1 : # 손이 1개 이상 감지되었을 경우

            #print(hands[0])
            #print(hands[1])
            location=hands[0]['lmList'] # 감지시킨 손의 각 포인트 좌표값 알아오기, GPC 파일에 손가락 위치 정보값 있음
            #location_ano=hands[1]['lmList']
            length_1, info_1, img_1 = detector.findDistance(location[4], location[8], img) # 엄지와 검지 값 받아오기
            #findDistance 함수를 열어 아래의 x1, y1, z1 = p1, x2, y2, z2 = p2 로 변경 필요.
            #length_2, info_2, img_2 = detector.findDistance(location_ano[4], location_ano[8], img)            
            #time.sleep(1)

            
            # 손 위치에 따라 볼륨 조절하기
            if length_1 < 50 : # 만약 검지와 엄지 사이의 값이 50 미만일 경우
                rel_x = location[4][1]/480 # 음량을 조절한다. 0 이하일 경우나, 1 이하일 경우에는 예외 처리하기
                if rel_x > 1 :
                    rel_x = 1
                elif rel_x < 0 :
                    rel_x = 0
                volume.SetMasterVolumeLevel(int(28*(1-rel_x)-28), None)#0:max~ -65:0 # 볼륨 조절 명령어
            #print(length_1)
            

        cv2.imshow('view', img) # 이미지를 화면에 출력

    if cv2.waitKey(1) == ord('q') : # q를 누르면 종료
        break