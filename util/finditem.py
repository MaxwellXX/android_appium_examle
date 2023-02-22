import numpy as np
import cv2
import imutils
from matplotlib import pyplot as plt


def find_layer1_in_map(screen_shot_path, visualized=True):
    """
    store目前只有一种颜色，通过颜色找到区域，再计算里面的圆形，返回中心点坐标
    :param screen_shot_path: 母图片位置
    :param visualized: 是否要把结果显示到窗体
    :return:
    """
    image = cv2.imread(screen_shot_path)
    lower_red = np.array([204,0,204])  # BGR-code of your lowest red
    upper_red = np.array([255,102,255])   # BGR-code of your highest red
    mask = cv2.inRange(image, lower_red, upper_red)
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 20, param1=20, param2=8,
                               minRadius=0, maxRadius=60)
    index = 0
    if circles is not None:
        output = image.copy()
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        coord = list()
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image,
            #   then draw a rectangle corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 0, 255), 2)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 51), -1)
            coord.append((int(x), int(y)))
            index = index + 1
        print('No. of circles detected = {}, coords: {}'.format(index, coord))

    if visualized:
        cv2.imshow('output', output)
        cv2.waitKey()
        cv2.destroyAllWindows()

    return coord

def find_layer2_in_map(screen_shot_path, visualized=True):
    """
    venue有多种颜色，且形状不一，要先找到轮廓，再找到封闭图形计算中心点
    :param screen_shot_path: 母图片位置
    :param visualized: 是否要把结果显示到窗体
    :return:
    """
    image = cv2.imread(screen_shot_path)
    brand = [(0, 0, 204), (0, 0, 255)]
    luxury = [(205, 5, 185 ), (208, 6, 189)]
    premium = [(170, 60, 245), (175, 64, 247)]
    value = [(25, 140, 245), (28, 142, 247)]
    local = [(0, 179, 0),(5, 180, 5)]
    noposition = [(155,140, 165), (160,141, 168)]
    openning = [(121,0, 0),(125,5, 5)]
    future12 = [(0, 0, 255),(5, 5, 255)]
    futer13 = [(40, 148, 255),(45, 150, 255)]

    position = [brand, luxury, premium, value, local, noposition, openning, future12, futer13]
    coord = list()
    all_cnts = list()
    for lower, upper in position:
        mask = cv2.inRange(image, lower, upper)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        #print("I found {} shapes".format(len(cnts)))
        if cnts:
            for c in cnts:
                if visualized:
                    all_cnts.append(c)
                M = cv2.moments(c)
                if M["m00"] == 0:
                    continue
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                coord.append((cX, cY))
    print(len(coord), coord)
    if visualized:
        for c in all_cnts:
            # draw the contour and show it
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return coord


if __name__ == '__main__':
    find_venue()