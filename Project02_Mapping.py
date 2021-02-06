import KeyPressModule as kp
from djitellopy import tello
import cv2
import numpy as np
import math
from time import sleep

###### Parameter ########
fSpeed = 117 / 10 #(15cm/s)
aSpeed = 360 / 10 #(50d/s)##!!!!!!!!!!!
interval = 0.25 # every unit on our map will skeching by 0.25 sec
dInterval = fSpeed * interval # 한 단위 즉 0.25초의 속도. ## 1초에 10미터 -> 0.25초에 2.5미터 라고 다르게 표현
aInterval = aSpeed * interval
#########################
point = []
x, y = 640, 360 # final value, 좌표 of 드론
a = 0 # 앵글은 0으로 리셋되면 안되는 반면 거리는 한 단위 움직인 후(좌표 갱신 이후)에는 리셋 되야함
yaw = 0

kp.init()
# drone = tello.Tello()
# drone.connect()
# print(drone.get_battery())


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    # speed = 50
    speed = 15
    aSpeed = 50
    d = 0
    global yaw, x, y, a           # wow 왜 에러 해결된건지, 변수 범위로 설명가능?

    if kp.get_key('LEFT'):      # if-elif-elif-elif-elif-elif-elif-elif-elif 에서 수정 1/28/2021 pm 3:24
        lr = -speed             # 이전에 키보드로 조작할 때 반대로 회전했던 겄같음 하여 + - 바꿈
        d = dInterval
        a= -180                 # Question : 여기서 왜 a(앵글)를 수정하지?? 방향은 안바뀌는데
    elif kp.get_key('RIGHT'):
        lr = speed
        d = -dInterval
        a = 180
    if kp.get_key('UP'):
        fb = +speed
        d = dInterval
        a = 270
    elif kp.get_key('DOWN'):
        fb = -speed
        d = -dInterval
        a= -90
    if kp.get_key('w'):
        ud = +speed
    elif kp.get_key('s'):
        ud = -speed
    if kp.get_key('a'):
        yv = -aSpeed
        yaw -= aInterval
    elif kp.get_key('d'):
        yv = +aSpeed
        yaw += aInterval
    if kp.get_key('q'):
        drone.land()
    if kp.get_key('e'):
        drone.takeoff()
    sleep(interval)
    a += yaw
    x += int(d*math.cos(math.radians(a)))
    y += int(d*math.sin(math.radians(a)))


    return [lr, fb, ud, yv, x, y]


def drawPoint(img, point): # x,y 두개 변수 대신 point라는 이름의 튜플 사용
    for dot in point:
        cv2.circle(img, dot, 3, (0,0,255), cv2.FILLED)
    cv2.circle(img, point[-1], 5, (0, 255, 0), cv2.FILLED)
                        #point
    cv2.putText(img, f'({(point[-1][0] - 640) / 100 } {((point[-1][1] - 360)*-1)/100 })m', (point[-1][0] +10, point[-1][1] +30), 1, 1, (0, 255, 0))

while True:
    vals = getKeyboardInput()
    print(vals)
    # drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = np.zeros((720,1280, 3), np.uint8)    # np.unit8 : Unsigned Integer -> 1000x1000 픽셀 3 layer 각각이 8비트 무부호 정수로 표현되는 numpy 영행렬 생성 -> img 객체 레퍼런스로 받음
    point.append((vals[4], vals[5]))                #point = (vals[4], vals[5]) 굳이 바꿀 이유가?
    drawPoint(img, point)
    cv2.imshow('Map of Drone', img)
    cv2.waitKey(1)