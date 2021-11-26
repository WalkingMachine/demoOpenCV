import cv2
import mediapipe as mp
import time
from pynput.keyboard import Key, Controller
import serial


arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.2)

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

frameWidth = 640
frameHeight = 480                              
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)


pTime = 0

bounceTime = 3
countToBounce = 0

import requests
from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict()


changeNeed = False

keyboard = Controller()

def release():
    print("release")
    #keyboard.release(Key.left)
    #keyboard.release(Key.right)
    #keyboard.release(Key.space)

def pressLeft():
    #keyboard.press('b')
    #keyboard.press(Key.enter)
    arduino.write(bytes('a', 'utf-8'))

def pressRight():
    #keyboard.press('a')
    #keyboard.press(Key.enter)
    arduino.write(bytes('b', 'utf-8'))


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            #print(id, lm)
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

    #print(results.pose_landmarks.landmark[0].x)
    if results.pose_landmarks:              
        if(results.pose_landmarks.landmark[15].visibility >0.8 ):
            if(results.pose_landmarks.landmark[15].y < results.pose_landmarks.landmark[13].y < results.pose_landmarks.landmark[11].y):
                print("Toggle")

        if results.pose_landmarks.landmark[0].visibility > 0.8:
            if results.pose_landmarks.landmark[0].y < 0.3:
                print("middle")
                keyboard.press(Key.space)
            elif results.pose_landmarks.landmark[0].x > 0.7:
                pressLeft()
            elif results.pose_landmarks.landmark[0].x < 0.3:
                pressRight()
            else:
                release()
        
    if(changeNeed):
    
        countToBounce +=1
        print("bouncing")
        if(countToBounce== bounceTime):
            print("--------------changing state-------------------")
            countToBounce =0
            changeNeed = False
            if(state=="on"):
                state ="off"
            else:
                state ="on"
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
              
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break