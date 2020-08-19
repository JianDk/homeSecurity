import json
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time

with open('diffValue.txt','r') as file:
    data = json.load(file)

diff_values = data[0]['frontCam2']['diff_value']
diff_values = np.array(diff_values)
files = np.array(data[0]['frontCam2']['files'])

#Use Otzu's method to find the optimal threshold. #Overall histogram
testImg = cv2.imread(files[1])
imgHeight = testImg.shape[0]
imgWidth = testImg.shape[1]
totalPixel = imgHeight * imgWidth
maxValue = totalPixel * 255

count, edges = np.histogram(diff_values, bins = 100, range = (0, 200000))
frequency = (count / np.sum(count)) * 100
edges = edges[:-1]
plt.plot(edges, frequency)
plt.draw()

class otzuThreshold:
    def __init__(self, arr):
        #get min and max of array
        self.minArr = np.min(arr)
        self.maxArr = np.max(arr)
        self.arr = arr
        
        sigmaWeight = np.array([])
        for i in range(int(self.minArr + np.array(1)), int(self.maxArr)):
            
            #Split the data set into two groups
            index = np.where(arr <= i)
            self.grp1 = arr[index]
            index = np.where(arr > i)
            self.grp2 = arr[index]
            self.i = i
            #All variables stored in class. 
            self.computeP()
            self.computeQ()
            self.computeMy()
            self.computeSigma()
            sigmaw = (self.q1 * self.sigma1) + (self.q2 * self.sigma2)
            sigmaWeight = np.append(sigmaWeight, sigmaw)
    
    def computeQ(self):
        #Compute probability in class 1
        self.q1 = self.p1.sum()
        self.q2 = self.p2.sum()
    
    def computeP(self):
        #Create bins and count the observations into each bins
        bins = np.arange(0, self.maxArr+2, 1)
        count = np.histogram(self.arr, bins, density = False)
        count = count[0]
        bins = bins[0:-1]
        self.bins1 = bins[0:self.i +1]
        self.bins2 = bins[self.i +1 :]
        self.p1 = count[0:self.i+1] / count.sum()
        self.p2 = count[self.i +1 :] / count.sum()
            
    def computeMy(self):
        my1 = (self.p1 * self.bins1) / self.q1
        self.my1 = my1.sum()
        
        my2 = (self.p2 * self.bins2) / self.q2
        self.my2 = my2.sum()
    
    def computeSigma(self):
        sigma1 = (self.bins1 - self.my1)**2
        sigma1 = (self.p1 / self.q1) * sigma1
        self.sigma1 = sigma1.sum()
        
        sigma2 = (self.bins2 - self.my2)**2
        sigma2 = (self.p2 / self.q2) * sigma2
        self.sigma2 = sigma2.sum()
        
th = otzuThreshold(diff_values)
