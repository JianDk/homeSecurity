from utils import motionDetection
from time import sleep
import os
from pathlib import Path
import json
import cv2

detectMotion = motionDetection()

for item in detectMotion.subStreamDirPaths:
    #Sort all files
    detectMotion._listTimeSortedFiles(item)
    folderIsEmpty = False
    
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
            
        detection,diff_value = detectMotion.motionDetectSingleCam(file1, file2, 230000)
        print(diff_value)
    
        if detection is True:
            img1 = cv2.imread(file1)
            img2 = cv2.imread(file2)
            print(diff_value)
            cv2.imshow('file1', img1)
            cv2.imshow('file2', img2)
            cv2.waitKey(5000)
        
            cv2.destroyAllWindows()
            