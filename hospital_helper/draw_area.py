import cv2
import numpy

"""
将划线区域提取出来
"""


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

stack = Stack()

def showImg(img_name, img):
    """图像显示"""
    cv2.imshow(img_name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()

def get_circle_point(x, y, circle):
    """
    以（x, y）为中心，circle从小至大向外扩展的矩形所包含的点
    即1*1方格的点，3*3方格内的点， 5*5方格内的点...
    :param x:
    :param y:
    :param circle:向外扩展幅度
    :return:返回从(x, y)向外每次以一格扩展的有序点的列表
    """
    point_list = [(x, y)]
    for i in range(1, circle+1):
        x_value = [x-i, x+i]
        y_value = [y-i, y+i]

        for y_ in range(y_value[0], y_value[1]+1):
            point_list.append((x_value[0], y_))
            point_list.append((x_value[1], y_))
        for x_ in range(x_value[0]+1, x_value[1]):
            point_list.append((x_, y_value[0]))
            point_list.append((x_, y_value[1]))
    return point_list

def get_around_point_value(x, y, mask, new_val, circle):
    """
    获取当前点，和区域范围内的值，以值为标准判断是否是区域内的值，是否触及边界
    如果不触及边界，则当前像素在封闭区间内，此像素涂上新色new_val, 并将此点入栈；
    若初触及边界，则停止，且不入栈。
    边界范围以（x, y)开始，最多向外扩展circle， 成为长宽为circle*circle+1的正方形
    :param x:
    :param y:
    :param mask:
    :param new_val:
    :return:
    """
    point_num = 0
    def push_popint(x, y, point_num):
        point_value = mask[x, y]
        if point_value == 255:
            point_num = point_num + 1
            return point_num
        if point_value == new_val:
            return point_num
        if point_num >= 1:
            if point_value == 255:
                pass
            else:
                mask[x, y] = new_val
        else:
            mask[x, y] = new_val
            stack.push((x, y))
        return point_num

    point_list = get_circle_point(x, y, circle)
    for x_, y_ in point_list:
        point_num = push_popint(x_, y_, point_num)  # one


def get_area(path, seed, line_color=(200, 50, 50)):
    """
    从某一路径获取图片，图片中线条颜色的大致范围，
    :param path:
    :param line_color:
    :return:
    """
    img = cv2.imread(path)

    # copy_img 复制图片做操作，原图像保留
    copy_img = img.copy()

    # 大致提取图中红色线条部分
    idx = numpy.where(copy_img[:, :, 2] > line_color[0], copy_img[:, :, 0] < line_color[1] , copy_img[:, :, 1] < line_color[2])
    # 不是红色线条的部分置为黑色
    copy_img[idx == False] = 0

    # 显示一下红色线条
    showImg("img_with_red_line", copy_img)

    # 二值化， 将红色线条部分变成白色
    ret, thresh = cv2.threshold(copy_img, 100, 200, 0)
    gray_thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    gray_thresh[gray_thresh!=0] = 255
    showImg("gray_thresh", gray_thresh)

    # 膨胀， 将线条断断续续处连接起来
    dilate_img = cv2.dilate(gray_thresh, (3, 3), 3)
    dilate_img = cv2.dilate(dilate_img, (3, 3), 3)
    dilate_img = cv2.dilate(dilate_img, (5, 5), 3)
    dilate_img = cv2.dilate(dilate_img, (7, 7), 3)
    showImg("dilate_img", dilate_img)

    # 掩模区域，初始化为膨胀后的有线条区域
    mask = dilate_img


    # 漫水
    stack.push(seed)
    # num = 1
    while not stack.isEmpty():
        point = stack.pop()  # 取出栈里的顶点
        x, y = point  # 点的下标
        try:
            get_around_point_value(x, y, mask, 100, 4)
        except Exception as e:
            raise Exception("画线区域不够封闭，请补充")
        # 每段时间看一次效果
        # if num % 200 == 0:
        #     showImg("mask", mask)
        # showImg("gray_thresh", gray_thresh)
        # num += 1

    result_img = img.copy()

    # 红色图像，用于涂色
    red_mask = numpy.zeros(img.shape, dtype='uint8')
    red_mask[:, :, 2] = 255

    # 涂上透明红色
    dst = cv2.addWeighted(result_img, 0.7, red_mask, 0.3, 0)

    # 显示画线联通区域内容
    red_res = cv2.bitwise_and(dst, dst, mask=mask)
    original_res = cv2.bitwise_and(result_img, result_img, mask=mask)
    showImg("red_res", red_res)
    showImg("original_res", original_res)


get_area("hospital.jpg", (370, 510))
