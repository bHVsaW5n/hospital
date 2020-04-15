"""
从一个封闭曲线内获取联通区域涂色

"""
import numpy as np
import cv2

from hospital_helper.my_stack import Stack


class ImgService:
    def __init__(self, path, circle=2, new_value=200):
        self.original_img = cv2.imread(path)  # 原图片
        self.gray_img = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY)
        self.stack = Stack()
        self.circle = circle
        self.new_value = new_value

    def show_img(self, img_name, img):
        cv2.imshow(img_name, img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def delete_unuseless_point(self, mask, threshold_value):
        """
        这里想去掉无用的不太联通的点
        :param mask:
        :return:
        """
        assert len(mask.shape) == 2
        copy_img = mask.copy()
        x_list, y_list = np.where(copy_img == 255)
        seed = (x_list[0], y_list[0])
        self.init_seed = seed
        self.stack.push(self.init_seed)  # 初始化种子放进去
        while not self.stack.isEmpty():
            x, y = self.stack.pop()
            judge_mask = mask[x-self.circle: x+self.circle, y-self.circle: y+self.circle]
            if len(judge_mask[judge_mask >= self.new_value]) <= threshold_value:
                mask[(x, y)] = 0
            else:
                mask[(x, y)] = self.new_value

                edge_seed_list = self._get_circle_point((x, y), self.circle)
                for around_point in edge_seed_list:  # 周围点
                    if mask[around_point] == 255:
                        self.stack.push(around_point)
        return mask



    def if_line_connected(self, mask, circle=2):
        """
        function:判断线条是否为联通区域, (width, height)
        thought: 对于线条内的一个点, 以此为基础
        mask: 线条的掩模, 线条为白色,  底为黑色
        :return:
        """
        # assert len(mask.shape) == 2
        # copy_img = mask.copy()
        # x_list, y_list = np.where(copy_img == 255)
        # seed = (x_list[0], y_list[0])
        # self.init_seed = seed
        self.stack.push((self.init_seed, None))  # 栈中存放(seed, last_seed) 放一个当前种子和上一个种子，标识他从上一个种子而来， 初始化种子没有上一个
        print("种子", (self.init_seed, None))
        return self._charge_if_edge(mask, 100, circle)

    def _charge_if_edge(self, mask, new_value, circle):
        """
        判断此点是否是边缘点
        :param mask:白色线条， 黑色底色的mask
        :param seed:当前点
        :param new_value: 若是边缘，则以新色替换原色，与原白色区分此像素是否已经被判断过
        :return:
        """
        # flag = True
        while not self.stack.isEmpty():
            seed, last_seed = self.stack.pop()
            first_seed = True
            if mask[seed] == 255:  # 是边缘, 当前点换新颜色, 判断周围点.  1:周围点为new_value，已考虑过  2:周围点为255, 入栈  3: 周围点为0， 不是边缘，不计
                mask[seed] = new_value  # 1: 边缘，换新色
                judge_mask = mask[seed[0]-circle:seed[0]+circle, seed[1]-circle:seed[1]+circle]
                if len(judge_mask[judge_mask>50]) <= 3:
                    # flag = False
                    print("不连通哦")
                    return mask
                edge_seed_list = self._get_circle_point(seed, circle)
                for around_point in edge_seed_list:  # 周围点
                    around_point_value = mask[around_point]
                    if around_point_value == 255:
                        self.stack.push((around_point, seed))
                    else:
                        pass
                    # if around_point == self.init_seed and last_seed != self.init_seed:
                    #     charge_area = mask[self.init_seed[0]-2:self.init_seed[0]+2, self.init_seed[1]-2:self.init_seed[1]+2]
                    #     if len(charge_area[charge_area == 255]) == 0:
                    #         print("这图是封闭的")
                    #         return mask
                    #     else:
                    #         pass
                            # print("这图是封闭的")
        print("这图不是封闭的")
        return mask
        # self.show_img("mask", mask)
        # return mask
                    # if around_point == self.init_seed and first_seed != True:
                    #     return True, mask
                    # first_seed = False

    def _get_circle_point(self, seed, circle):
        """
        以（x, y）为中心，circle从小至大向外扩展的矩形所包含的点
        即1*1方格的点，3*3方格内的点， 5*5方格内的点...
        :param x:
        :param y:
        :param circle:向外扩展幅度
        :return:返回从(x, y)向外每次以一格扩展的有序点的列表
        """
        x, y = seed
        point_list = []
        for i in range(1, circle + 1):
            x_value = [x - i, x + i]
            y_value = [y - i, y + i]

            for y_ in range(y_value[0], y_value[1] + 1):
                point_list.append((x_value[0], y_))
                point_list.append((x_value[1], y_))
            for x_ in range(x_value[0] + 1, x_value[1]):
                point_list.append((x_, y_value[0]))
                point_list.append((x_, y_value[1]))
        return point_list
