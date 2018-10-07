#!/usr/bin/env python

# _*_ coding:utf-8 _*_

'''

@author: diw

@contact: di.W@hotmail.com

@file: keyword_percent

@time: 2018/10/1 13:10

@desc:

'''

import topic_sta1
weibofilefolder = 'D:/chinadream/data'
file_path_list = topic_sta1.getAllFile(weibofilefolder)
topic_sta1.topic_keyword(file_path_list)