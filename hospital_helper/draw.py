# import stack

# -*- coding=GBK -*-
import cv2 as cv
import numpy as np


def showImg(img_name, img):
    cv.imshow(img_name, img)
    cv.waitKey()
    cv.destroyAllWindows()

# 指定颜色替换
def fill_image(image):
    copyImage = image.copy()  # 复制原图像
    h, w = image.shape[:2]  # 读取图像的宽和高
    mask = np.zeros([h + 2, w + 2], np.uint8)  # 新建图像矩阵  +2是官方函数要求

    cv.floodFill(copyImage, mask, (430, 240), (0, 100, 255), (100, 100, 50), (50, 50, 50), cv.FLOODFILL_FIXED_RANGE)

    showImg("copyImage", copyImage)
    result_mask = np.zeros(shape=copyImage.shape)
    ids = np.where((copyImage==(0, 100, 255)))
    result_mask[ids[:2]] = (255, 255, 255)
    mask = cv.inRange(result_mask, (200, 0, 0), (255, 255, 2555))
    # result_mask = cv.cvtColor(result_mask, cv.COLOR_BGR2GRAY)
    # cv.imshow("填充", copyImage)
    showImg("copyImage", copyImage)
    showImg("result_mask", result_mask)
    showImg("image", image)
    res = cv.bitwise_and(image, image, mask=mask)
    showImg("res", res)



src = cv.imread("hospital.jpg")
cv.imshow("原来", src)
showImg("src", src)
fill_image(src)
