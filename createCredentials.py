#This script is used to create camera credientials used and subsequentially saved in a json file
import json
cam1 = dict()
cam1['ip'] = '192.168.231.100'
cam1['port'] = 9000
cam1['rtsp_sub'] = 'rtsp://admin:password@192.168.231.100:554//h264Preview_01_sub'
cam1['rtsp_main'] = 'rtsp://admin:password@192.168.231.100:554//h264Preview_01_main'

camCred = dict()
camCred['frontCam1'] = cam1

with open('cred.txt','w') as file:
    json.dump(camCred,file)
