from email import header


#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File: feng_libs.py
@Time: 2022/05/05 15:52:37
@Author: Jim
@Contact: zhengwenfeng37@gmail.com
@Desc: 
'''


from feng_libs.file_libs.pdf_libs import PdfLibs


class FengLibs:

    def __init__(self):
        self.pdf_libs = PdfLibs()
