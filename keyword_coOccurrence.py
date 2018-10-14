# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/10/14 19:39
   Author  : diw
   Email   : di.W@hotmail.com
   File    : keyword_coOccurrence.py
   Desc:
-------------------------------
"""

import topic_sta1
weibofilefolder = 'D:/chinadream/data'
file_path_list = topic_sta1.getAllFile(weibofilefolder)
result_dic = topic_sta1.keyword_coOccurrence(file_path_list)
print(result_dic)