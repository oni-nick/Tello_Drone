import cv2
import numpy as np
import djitellopy
fbRange = [6200, 6800] # Number of pixel of face
pid = [0.4, 0.4, 0]  # If your drone is not work ideally then you tune these parameter
pError = 0
w, h = 640, 480  # Size of Image

def face_detection(img):
    faceCascade = cv2.CascadeClassifier('Resources/haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.3, 5)  # Recommended 1.2, 8
    # detectMultiScale() 메소드 파라미터 설명
    # https://towardsdatascience.com/a-guide-to-face-detection-in-python-3eab0f6b9fc1
    FaceListc = []
    FaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
        cx = x + w // 2
        cy = y + h //2
        area = w * h
        cv2.circle(img, (cx,cy), 5, (0,255,0), cv2.FILLED)
        FaceListc.append([cx,cy])
        FaceListArea.append(area)
    if len(FaceListArea) != 0:
        i = FaceListArea.index(max(FaceListArea))
        return img, [FaceListc[i], FaceListArea[i]]
    else:
        return img, [[0,0], 0]


def trackFace(info, w, pid, pError):
    x, y = info[0]
    area = info[1]
    fb = 0
    yaw_speed = 0
    error = x - w//2 # x is center of Face, w//2 is center of Image
    yaw_speed = pid[0] * error + pid[1] * (error - pError)
    yaw_speed = int(np.clip(yaw_speed, -100, 100))

    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:   # If drone is too close to man's face, then move backward, too close -> too big face in image
        fb = -20
    elif area < fbRange[0] and area != 0:  # < 연산만 쓰면 0인경우도 포함되기에 배제한것
        fb = 20

    if x == 0:              # 얼굴 감지 못했을때
        yaw_speed = 0
        error = 0

    print('전후진 :', fb, '회전각 : ', yaw_speed)
#    drone.send_rc_control(0, fb, 0, yaw_speed)
    return error


cam = cv2.VideoCapture(0)

while True:
    result, img = cam.read()                                     # print(result) # False면 cam.read() -> faulse
    img = cv2.resize(img, (w, h))  # 360 x 240
    img, info = face_detection(img)
    pError = trackFace(info, w, pid, pError)
    # print('Center : ', info[0], 'Area : ', info[1])               # cv2.circle(img, (300,300), 100, (0,0,255), cv2.BORDER_WRAP)
    cv2.imshow('Video Straming by Webcam', img)
    cv2.waitKey(1)