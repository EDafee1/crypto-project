import matplotlib.pyplot as plt #importing matplotlib
import cv2

img = cv2.imread('temp_img.png', 0)
histr = cv2.calcHist([img],[0],None,[256],[0,256])
plt.plot(histr)
plt.show()