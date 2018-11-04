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
weibofilefolder = '/Volumes/新加卷/chinadream/data'
file_path_list = topic_sta1.getAllFile(weibofilefolder)
topic_sta1.keyword_percent(file_path_list)