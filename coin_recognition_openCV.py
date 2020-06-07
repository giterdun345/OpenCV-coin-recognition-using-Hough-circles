# -*- coding: utf-8 -*-
"""
Created on Tue May 26 13:22:14 2020

@author: martin
"""

import cv2
import numpy as np

# import image blurring on and leaving another as is 
coins = cv2.imread(r'coins.png', cv2.IMREAD_GRAYSCALE)
original_image = cv2.imread('coins.png', 1)
coins = cv2.GaussianBlur(coins, (5,5), 0)

# ensure image loaded 
cv2.imshow('Image', original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# check image for grey 
cv2.imshow('Image', coins)
cv2.waitKey(0)
cv2.destroyAllWindows()

# input desired calculations from grid search, see notebook
circles = cv2.HoughCircles(coins,
                           cv2.HOUGH_GRADIENT,
                           dp = 1.2,
                           minDist = 115,
                           param1=50,
                           param2 = 26, 
                           minRadius = 20,
                           maxRadius = 100
                          )

# rounds values output by hough function and displays the mount of circles
circles = [np.rint(circle)for circle in circles]

# Obtain average brightness within each circle
brightness = []
for circle in circles[0]:
    lowerx = int(circle[1] - 5)
    upperx = int(circle[1] + 5)
    lowery = int(circle[0] - 5)
    uppery = int(circle[0] + 5)
    average_brightness = original_image[lowerx:upperx, lowery:uppery].mean()
    brightness.append(round(average_brightness,2))
    
# count for indexing/ reference
count = 0
# loop over the (x, y) coordinates and radius of the circles
for (x, y, r) in circles[0]:
    # keeps count of the coin
    count +=1
    # draw the circle in the output image, then draw a rectangle
    # corresponding to the center of the circle
    cv2.circle(original_image, (x, y), r, (0,0,255), 3 )
    leftx = int(x - 5)
    lefty = int(y - 5)
    rightx = int(x + 5)
    righty = int(y + 5)
    cv2.rectangle(original_image, (leftx, lefty), (rightx, righty), (0, 128, 255), -1)

#     deciding which coin is which by radii and brightness
    if r > 67 and r < 70 and brightness[count-1] <= 94:
        coin = 2
    elif r > 55 and brightness[count-1] > 200:
        coin = 10
    elif r > 52 and r < 57 and brightness[count-1] > 75 and brightness[count-1] < 121:

        coin = 1
    elif r > 50 and r < 67 and brightness[count-1] > 170:

        coin = 5 
    else:

        coin = 100
    # PLace text
    cv2.putText(original_image, (str(coin) + ' Pence'), (x,y), cv2.FONT_HERSHEY_SIMPLEX , 1, (255, 0, 0), 2)

    
# displaying the circles
cv2.imshow("Results", original_image)

cv2.waitKey(0)
cv2.destroyAllWindows()