import json
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time

with open('diffValue.txt','r') as file:
    data = json.load(file)

diff_values = data[0]['frontCam1']['diff_value']
diff_values = np.array(diff_values)
files = np.array(data[0]['frontCam1']['files'])

#Use Otzu's method to find the optimal threshold. #Overall histogram
#testImg = cv2.imread(files[1])
#imgHeight = testImg.shape[0]
#imgWidth = testImg.shape[1]
#totalPixel = imgHeight * imgWidth
#maxValue = totalPixel * 255

count, edges = np.histogram(diff_values, bins = 1000, range = (0, 17700001))
frequency = (count / np.sum(count)) * 100
edges = edges[:-1]
plt.plot(edges, frequency)
plt.show()

class otzuThreshold:
    def __init__(self, arr):
        #get min and max of array
        self.minArr = np.min(arr)
        self.maxArr = np.max(arr)
        self.arr = arr
        
        self.sigmaWeight = np.array([])
        self.createP()
        self.thresholdValues = np.arange(self.minArr +1, self.maxArr, 100000, dtype = int)
        print(len(self.thresholdValues))
        for i in self.thresholdValues:
            self.i = i
            #All variables stored in class. 
            self.computeP()
            self.computeQ()
            self.computeMy()
            self.computeSigma()
            sigmaw = (self.q1 * self.sigma1) + (self.q2 * self.sigma2)
            self.sigmaWeight = np.append(self.sigmaWeight, sigmaw)
            
            print(i)
            
    def computeQ(self):
        #Compute probability in class 1
        self.q1 = self.p1.sum()
        self.q2 = self.p2.sum()
    
    def createP(self):
        #Create bins and count the observations into each bins
        bins = np.arange(0, self.maxArr+2, 1)
        count = np.histogram(self.arr, bins, density = False)
        self.Totalcount = count[0]
        self.Totalbins = bins[0:-1]
        
    def computeP(self):
        self.bins1 = self.Totalbins[0:self.i +1]
        self.bins2 = self.Totalbins[self.i +1 :]
        
        self.p1 = self.Totalcount[0:self.i+1] / self.Totalcount.sum()
        self.p2 = self.Totalcount[self.i +1 :] / self.Totalcount.sum()
            
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
cam1 = dict()
cam1['threshold'] = th.thresholdValues.tolist()
cam1['weightedSigma'] = th.sigmaWeight.tolist()

plt.plot(cam1['threshold'], cam1['weightedSigma'])
plt.draw()
plt.show()

#Save the data
with open('sigmaw_cam1.txt', 'w') as file:
    json.dump(cam1, file, indent = 4)

print('complete')