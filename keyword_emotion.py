# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/11/4 下午11:07
   Author  : diw
   Email   : di.W@hotmail.com
   File    : keyword_emotion.py
   Desc:
-------------------------------
"""
import topic_sta1
from topic_sta1 import weibofilefolder

if __name__=='__main__':

     file_path_list = topic_sta1.getAllFile(weibofilefolder)
     topic_sta1.keyword_emotion(file_path_list)