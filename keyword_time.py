# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/11/4 20:14
   Author  : diw
   Email   : di.W@hotmail.com
   File    : keyword_time.py
   Desc:
-------------------------------
"""

import topic_sta1



if __name__=='__main__':
     #lda
     file_path_list = topic_sta1.getAllFile(topic_sta1.weibofilefolder)
     #输出结果
     topic_sta1.keyword_time(file_path_list)