import cv2
import mediapipe as mp
import math
import numpy

from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

video = cv2.VideoCapture(0)


while True:
    success,img = video.read()

    #detecting hands
    result = hands.process(img)


    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lmList=[]
            for id,lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                
                mp_drawing.draw_landmarks(img,handLms, mp_hands.HAND_CONNECTIONS)

        if lmList:
            x1,y1 = lmList[4][1],lmList[4][2]
            x2,y2 = lmList[8][1],lmList[8][2]
            cv2.circle(img,(x1,y1),15,(1,23,123),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(1,23,123),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(1,23,123),4)
            length = math.hypot(x2-x1,y2-y1)

            volrange = volume.GetVolumeRange()
            minvol = volrange[0]
            maxvol = volrange[1]
            vol = numpy.interp(length, [50,100] , [minvol, maxvol])
            
            volPer = numpy.interp(length, [50,100] ,[0,100])
            volBar = numpy.interp(length,[50,300],[400,150])

            volume.SetMasterVolumeLevel(vol,None)
            cv2.putText(img,str(int(volPer)),(40,450),cv2.FONT_HERSHEY_COMPLEX,2,(1,3,5),3)
            cv2.rectangle(img,(50,150),(85,400),(123,213,122),3)
            cv2.rectangle(img,(50,int(volBar)),(85,400),(0,231,23),cv2.FILLED)
            

    cv2.imshow("Wireless Sound Control",img)
    cv2.waitKey(1)
