#!/usr/bin/env python

# _*_ coding:utf-8 _*_

'''

@author: diw

@contact: di.W@hotmail.com

@file: topic_follower

@time: 2018/9/29 20:42

@desc:

'''
import topic_sta1
weibofilefolder = 'D:/chinadream/data'
file_path_list = topic_sta1.getAllFile(weibofilefolder)
topic_sta1.topic_percent(file_path_list)
