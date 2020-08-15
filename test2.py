from utils import Stream, garbageCollect, motionDetection
import json
from threading import Thread
from time import sleep

#cam parameters
with open('cred.txt','r') as file:
    cred = json.load(file)
    
cam1StreamSub = Stream(camName = 'frontCam1',
                       rtsp = cred['frontCam1']['rtsp_sub'],
                       rtspSource = 'sub',
                       sec_betweenFrame = 1)

cam2StreamSub = Stream(camName = 'frontCam2',
                       rtsp = cred['frontCam2']['rtsp_sub'],
                       rtspSource = 'sub',
                       sec_betweenFrame = 1) #0.5 sec between frame sampling

cam1StreamThread = Thread(target = cam1StreamSub.stream)
cam2StreamThread = Thread(target = cam2StreamSub.stream)

cam1StreamThread.start()
cam2StreamThread.start()
secToWait = 60 * 60 *24
sleep(secToWait)
cam1StreamSub.closeStream()
cam2StreamSub.closeStream()
print('complete')

    
    
    
    
