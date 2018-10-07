#!/usr/bin/env python

# _*_ coding:utf-8 _*_

'''

@author: diw

@contact: di.W@hotmail.com

@file: topic_location

@time: 2018/9/29 2:37

@desc:

'''

import topic_sta1
weibofilefolder = 'D:/chinadream/data'
file_path_list = topic_sta1.getAllFile(weibofilefolder)
topic_sta1.keyword_location(file_path_list)
