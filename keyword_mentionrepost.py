# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2019-04-27 16:13
   Author  : diw
   Email   : di.W@hotmail.com
   File    : keyword_mentionrepost.py
   Desc:    count mention rate and repost rate
-------------------------------
"""

from topic_sta1 import keyword_mentionrepost,getAllFile
weibofilefolder = '/Volumes/elementary/chinadream/data'

if __name__ == '__main__':
    file_list = getAllFile(weibofilefolder)
    keyword_mentionrepost(file_list)

