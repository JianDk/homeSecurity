from utils import motionDetection
from time import sleep
import os
from pathlib import Path
import json

detectMotion = motionDetection()
camDict = dict()
camList = list()

for item in detectMotion.subStreamDirPaths:
    #Sort all files
    detectMotion._listTimeSortedFiles(item)
    folderIsEmpty = False
    cam = Path(item).parents[0]
    cam = os.path.basename(cam)
    camDict[cam] = dict()
    camDict[cam]['files'] = list()
    camDict[cam]['diff_value'] = list()
    
    while folderIsEmpty is False:
        if detectMotion.list_of_files:
            file1 = detectMotion.list_of_files[0]
            detectMotion.list_of_files.pop(0)
        else:
            folderIsEmpty = True
        
        if detectMotion.list_of_files:
            file2 = detectMotion.list_of_files[0]
            detectMotion.list_of_files.pop(0)
        else:
            folderIsEmpty = True
            
        _, diff_value = detectMotion.motionDetectSingleCam(file1, file2, 200000)
        camDict[cam]['files'].append(file1)
        camDict[cam]['diff_value'].append(diff_value)
    
    camList.append(camDict)

#save the file
with open('diffValue.txt','w') as file:
    json.dump(camList, file, indent=4)
print('complete')