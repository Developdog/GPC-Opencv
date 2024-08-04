"""
python 3.10.0
pip install opencv-python
pip install numpy
pip install tensorflow tf
"""

import cv2
import numpy as np
import tensorflow as tf # 현재 케라스는 tensorflow에 합병됨

#import time

import os

#print(os.getcwd()) # python 실행 위치 확인하기
#os.chdir('./GPC') # 확인 후 실행 위치 변경하기

cap = cv2.VideoCapture(0) # 열린 웹캠의 정보 값을 cap에 전달
model=tf.keras.models.load_model('keras_model.h5', compile=False) # teachable machine에서 가져온 모델값을 가져온다.
classes = ['nail polish', 'holder', 'nothing']

while cap.isOpened : # 카메라가 연결되었을 경우
    ret, img = cap.read() # 카메라로부터 이미지를 읽어옴
    if ret : # 이미지를 읽었을 경우
        img = cv2.flip(img, 1) # 이미지 좌우 반전
        img = img[:480, 80:560] # 이미지를 480x480으로 자름 
        #뒤의 값을 80:560은 일반적으로 480,480일 경우 세로 카메라의 값이 눌리는 경우가 있기 때문이다.
        img = cv2.resize(img, (224, 224)) # 케라스 모델에 적용하기 위해 크기변환

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 이미지 색상을 BGR에서 RGB로 변경
        img_input = img.astype(np.float32)/127.0 - 1 # 이미지를 0 ~ 1사이의 값으로 변경
        # 모든 수치의 값들이 0 ~ 255의 사이이기 떄문에, 127로 나누면 0 ~ 2 의 값이 되고, 여기서
        # 1을 뺴줌으로써 평균값이 0이 되도록 만드는 방법을 실행한다.



        img_input=np.expand_dims(img_input, axis = 0)
        # 이미지 데이터에 배치 차원을 추가한다.
        # 딥러닝 모델은 일반적으로 배치 단위로 데이터를 처리하므로, 단일 이미지라도 배치 차원을 추가 필요.
        predict=model.predict(img_input) # 이미지를 모델에 넣어 예측
        
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) # 이미지 다시 변환
        img = cv2.resize(img, (480, 480)) # 이미지 다시 색 변경

        idx = np.argmax(predict) # predict에서 가장 높은 값의 인덱스 값을 출력하기

        cv2.putText(img, text = classes[idx], org = (10, 30), 
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                    fontScale=1, 
                    color=(0,0,255), 
                    thickness = 2)
        # 왼쪽 상단에 현재 predict 값이 지정하는 변수값 출력시키기
        print(classes[idx])



        cv2.imshow('camera', img) # 이미지를 화면에 출력
        #h,w,c = img.shape # 이미지의 높이, 너비, 채널을 받아옴
        #print(h,w,c) #@ 이미지의 높이, 너비, 채널을 출력

    if cv2.waitKey(1) == ord('q') : # q를 누르면 종료
        break
