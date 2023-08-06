#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File: pdf_libs.py
@Time: 2022/05/05 15:48:41
@Author: Jim
@Contact: zhengwenfeng37@gmail.com
@Desc:  pdf工具
'''

import os
from PyPDF2 import PdfFileMerger


class PdfLibs:
    """pdf工具

    """

    @staticmethod
    def get_pdf_list(dir_path: str):
        """ 获取目录下的所有pdf文件

        dir_path: 文件路径
        """
        pdf_files = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))

        print("添加执行顺序: {}".format(pdf_files))
        return pdf_files

    @staticmethod
    def merge(input_dir_path: str, output_file_name: str) -> bool:
        """合并目录下的素有pdf文件，并且输出到指定目录中

        Args:
            input_dir_path (str): 输入文件夹路径
            output_file_name (str): 输出文件名称

        Returns:
            bool: 是否合并成功

        """
        merge_path_file = os.path.join(input_dir_path, output_file_name)
        if os.path.exists(merge_path_file):
            print("合并失败，输出文件已存在")
            return

        file_merger = PdfFileMerger()
        for pdf_file in PdfLibs.get_pdf_list(input_dir_path):
            file_merger.append(pdf_file)

        file_merger.write(merge_path_file)
        print("合并完成")


if __name__ == '__main__':
    PdfLibs.merge("C:\\Users\\User\\Downloads\\pdf", "merge.pdf")
