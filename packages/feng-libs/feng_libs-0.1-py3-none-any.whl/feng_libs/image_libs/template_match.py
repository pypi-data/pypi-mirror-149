# -*- coding: utf-8 -*-

__author__ = 'Jim'

import cv2
import numpy as np
from typing import Union, List


class TemplateMatch:
    """
        用来实现模板匹配

        在图片中查找模板图片的位置。
    """

    @staticmethod
    def find_template_pos_debug(aim_img: str, template_img: str, method: int = cv2.TM_CCOEFF_NORMED,
                                score: int = 0.8) -> None:
        """
        测试匹配效果


        :param aim_img: 目标图片路径
        :param temp_img: 模板图片路径
        :param method: 选择使用的算法。
        可以先进行测试，然后选择合适的算法使用。

        :param score: 分数。选择匹配相似度。
        :return:
        """

        aim_img = cv2.imread(aim_img, 0)
        template_img = cv2.imread(template_img, 0)

        h, w = template_img.shape[:2]

        for pos in TemplateMatch.find_template_pos(aim_img, template_img, method, score):
            cv2.rectangle(aim_img, pos, (pos[0] + w, pos[1] + h), 0, 2)

        cv2.imshow("demo", aim_img)
        cv2.waitKey(0)

    @staticmethod
    def find_template_pos(aim_img: Union[str, np.ndarray], template_img: Union[str, np.ndarray],
                          method: int = cv2.TM_CCOEFF_NORMED, score: int = 0.8) -> List:
        """
        在目标图片中匹配多个, 获取匹配的左上角坐标

        :param aim_img: 目标图片路径
        :param temp_img: 模板图片路径
        :param method: 选择使用的算法。
        可以先进行测试，然后选择合适的算法使用。

        :param score: 分数。选择匹配相似度。
        :return: list(左上角坐标集合)
        """

        if isinstance(aim_img, str):
            aim_img = cv2.imread(aim_img, 0)
        if isinstance(template_img, str):
            template_img = cv2.imread(template_img, 0)

        result_pos = []

        res = cv2.matchTemplate(aim_img, template_img, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= score)
        for pt in zip(*loc[::-1]):
            result_pos.append(pt)

        return result_pos

    @staticmethod
    def find_template_pos_test_method(aim_img: str, template_img: str) -> None:
        """
        测试使用哪种算法匹配更准确
        :param aim_img:
        :param template_img:
        :return:
        """

        img = cv2.imread(aim_img, 0)
        img2 = img.copy()
        template = cv2.imread(template_img, 0)
        w, h = template.shape[::-1]

        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                   'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        for meth in methods:
            img = img2.copy()
            method = eval(meth)

            # Apply template Matching
            res = cv2.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            cv2.rectangle(img, top_left, bottom_right, 0, 2)

            cv2.imshow(meth, img)
            cv2.waitKey(0)


if __name__ == '__main__':
    # TemplateMatch.find_template_pos_test_method("../../images/aim.jpg", "../../images/template.png")

    TemplateMatch.find_template_pos_debug("../../images/aim.jpg", "../../images/template.png", score=0.58)
