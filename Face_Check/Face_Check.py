import cv2

# 세그멘테이션 모듈 불러오기 (블러 처리용)
from cvzone.SelfiSegmentationModule import SelfiSegmentation as ssm

# 세그멘테이션 모듈 객체 생성
segmentor = ssm()

# 사전 훈련된 Haar Cascade 분류기 파일 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 웹캠 캡처 객체 생성
cap = cv2.VideoCapture(0)

while cap.isOpened :
    # 웹캠에서 프레임 읽기
    ret, img = cap.read()
    
    # 그레이스케일 이미지로 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 얼굴 인식
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) :
        img_blur = cv2.GaussianBlur(img, (51, 51), 0)  # 원본 이미지 블러 처리
        img = segmentor.removeBG(img, imgBg=img_blur) # 블러 처리 실행

    # 얼굴 주변에 사각형 그리기
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # 결과 이미지 출력
    cv2.imshow('Face Detection', img)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 해제
cap.release()
cv2.destroyAllWindows()