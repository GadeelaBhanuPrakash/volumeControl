import cv2
import mediapipe as mp
import math
import numpy as np

mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils

from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
volRange= volume.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]

cap=cv2.VideoCapture(0)

while True:
    success,img=cap.read()
    results=hands.process(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmlist=[]
            for id,lm in enumerate(handLms.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmlist.append([id,cx,cy])
                #mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
            if lmlist:
                x1,y1=lmlist[4][1],lmlist[4][2]
                x2,y2=lmlist[8][1],lmlist[8][2]
                cv2.circle(img,(x1,y1),15,(25,0,25),cv2.FILLED)
                cv2.circle(img,(x2,y2),15,(25,0,25),cv2.FILLED)

                z1=(x1+x2)//2
                z2=(y1+y2)//2
                length=math.hypot(x2-x1,y2-y1)

                if length<50:
                    cv2.circle(img,(z1,z2),15,(2,0,55),cv2.FILLED)

            vol=np.interp(length,[50,150],[minVol,maxVol])
            volBar=np.interp(length,[50,150],[400,150])
            volPer=np.interp(length,[50,150],[0,100])
            volume.SetMasterVolumeLevel(vol,None)
            cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
            cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
            cv2.putText(img,f"{int(volPer)}%",(40,450),cv2.FONT_HERSHEY_COMPLEX,3,(0,123,12),3)
    
    cv2.imshow('Image',img)
    cv2.waitKey(1)