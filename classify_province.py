# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/10/17 18:56
   Author  : diw
   Email   : di.W@hotmail.com
   File    : classify_province.py
   Desc:
-------------------------------
"""

import topic_sta1
weibofilefolder = 'D:/chinadream/data'
file_path_list = topic_sta1.getAllFile(weibofilefolder)
topic_sta1.classify_Province(file_path_list)