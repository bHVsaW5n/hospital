import cv2
import numpy


# 显示图片
def showImg(img_name, img):
    cv2.imshow(img_name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def get_outline(path):
    """
    从一张医疗影像中画出该医疗影像中涂色区域
    :param path:影响图片路径
    :return:
    """
    # 读取图片
    original_img = cv2.imread(path)
    copy_img = original_img.copy()
    showImg("original_img", original_img)

    # 医疗影像为黑白图， rgb值相等， 涂色区域rgb三个值不想等，以此为依据，将涂色区域提取出来
    index = numpy.where(
        (original_img[:, :, 2] == original_img[:, :, 1]) & (original_img[:, :, 2] == original_img[:, :, 0]))
    zero_index = numpy.where(
        (original_img[:, :, 2] != original_img[:, :, 1]) | (original_img[:, :, 2] != original_img[:, :, 0]) | (
                    original_img[:, :, 1] != original_img[:, :, 0]))

    # 将提取出来的涂色区域变为白色，不计入区域置为黑色
    original_img[index] = (255, 255, 255)
    original_img[zero_index] = (0, 0, 0)

    # 将图像转为灰度图像
    gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    # 以一张空白黑色图像为背景，后期将轮廓放上去， 最终形成黑底蓝边界的 边界图像
    black_img = numpy.zeros(original_img.shape)

    # 边缘提取
    image, contours, hierarchy = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    useful_contours = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if original_img.shape[0] - w < 10 and original_img.shape[1] - h < 10:
            pass
        else:
            useful_contours.append(cnt)
    cv2.drawContours(black_img, useful_contours, -1, (255, 0, 0), 2)
    cv2.drawContours(copy_img, useful_contours, -1, (255, 0, 0), 2)

    showImg("black_img", black_img)
    showImg("copy_img", copy_img)
    return black_img



get_outline("aa.png")
