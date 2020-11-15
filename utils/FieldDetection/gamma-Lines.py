import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt
import sys
import math

figsize = (100, 100)

# field area
x = []
y = []

# show RGB
img = cv2.imread('0.jpg')
RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.figure(figsize=figsize)
plt.imshow(RGB, cmap="gray", vmin=0, vmax=255)
plt.show()

# show gamma
alpha = 2  # a*F(x) + b
beta = 100
gamma = cv2.addWeighted(RGB, alpha, np.zeros(RGB.shape, RGB.dtype), 0, beta)
plt.figure(figsize=figsize)
plt.imshow(gamma, cmap="gray", vmin=0, vmax=255)
plt.show()

# show gray
img_copy = np.copy(RGB)
img_gray = cv2.cvtColor(gamma, cv2.COLOR_BGR2GRAY)
plt.figure(figsize=figsize)
plt.imshow(img_gray, cmap="gray", vmin=0, vmax=255)
plt.show()

# morph
# imgDilation = cv2.dilate(img_gray, kernel, iterations=1)
# plt.figure(figsize=figsize)
# plt.imshow(imgDilation, cmap="gray", vmin=0, vmax=255)
# plt.show()
# res, binary = cv2.threshold(img_gray, 20, 255, cv2.THRESH_BINARY)
# plt.figure(figsize=figsize)
# plt.imshow(binary, cmap="gray", vmin=0, vmax=255)
# plt.show()
# closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
# plt.figure(figsize=figsize)
# plt.imshow(closing, cmap="gray", vmin=0, vmax=255)
# plt.show()
# blur
# blur = cv2.GaussianBlur(img_gray, (7, 7), cv2.BORDER_DEFAULT)
# plt.figure(figsize=figsize)
# plt.imshow(img_gray, cmap="gray", vmin=0, vmax=255)
# plt.show()
# show opening
# edges

# show threshold
res, binary = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
plt.figure(figsize=figsize)
plt.imshow(binary, cmap="gray", vmin=0, vmax=255)
plt.show()

edges = cv2.Canny(binary, 1, 255)
plt.figure(figsize=figsize)
plt.imshow(edges, cmap="gray", vmin=0, vmax=255)
plt.show()

# kernel
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# HoughLinesP
rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 1  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 500  # minimum number of pixels making up a line
max_line_gap = 150  # maximum gap in pixels between connectable line segments
# line_image = np.copy(img) * 0  # creating a blank to draw lines on

linesP = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
if linesP is not None:
        length = len(linesP)
        for i in range(0, length):
            l = linesP[i][0]
            cv2.line(img_copy, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)
            x.append(l[0])
            x.append(l[2])
            if 250 < l[0] < 650:
                y.append(l[1])
            if 1300 < l[2] < 1750:
                y.append(l[3])
if linesP is not None:
    cv2.putText(img_copy, " Field Area", (1600, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    cv2.rectangle(img_copy, (1600, 55), (1800, 150), (0, 0, 255), 2)
    # field area
    cv2.putText(img_copy, str(min(x)), (1600, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(img_copy, str(max(x)), (1745, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(img_copy, str(min(y)), (1810, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(img_copy, str(max(y)), (1810, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

plt.figure(figsize=figsize)
plt.imshow(img_copy, cmap="gray", vmin=0, vmax=255)
plt.show()

# cv2.imshow("mask", image)
# cv2.waitKey(0)