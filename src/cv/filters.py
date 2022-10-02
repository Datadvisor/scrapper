import cv2
import numpy as np


def filter_resize(img):
    return cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)


def filter_threshold(img):
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.bilateralFilter(img, 9, 75, 75)
    cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return img


def filter_kernel(img):
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    return img


def filter_blackText(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_val = np.array([0, 0, 0])
    upper_val = np.array([179, 100, 130])

    mask = cv2.inRange(hsv, lower_val, upper_val)
    res = cv2.bitwise_and(img, img, mask=mask)
    return filter_threshold(res)


def filter_whiteText(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_val = np.array([0, 0, 100])
    upper_val = np.array([20, 20, 65])

    mask = cv2.inRange(hsv, lower_val, upper_val)
    res = cv2.bitwise_not(mask)
    return filter_threshold(res)

filters_dictionary = {
        "resize": filter_resize,
        "threshold": filter_threshold,
        "kernel": filter_kernel,
        "whiteText": filter_whiteText,
        "blackText": filter_blackText
    }