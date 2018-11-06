# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/11/6 10:25
   Author  : diw
   Email   : di.W@hotmail.com
   File    : keyword_emotion_time.py
   Desc:
-------------------------------
"""
import topic_sta1
from topic_sta1 import keywords_list
from math import log

def get_data():
    file_path_list = topic_sta1.getAllFile(topic_sta1.weibofilefolder)
    # 输出结果
    topic_sta1.keyword_emotion_time(file_path_list)

if __name__ == '__main__':
    #get result_data
    result_data = get_data()