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
weibofilefolder = '/home/diw/chinadream/data'

if __name__ == '__main__':
    file_list = getAllFile(weibofilefolder)
    mention_repost_dic = keyword_mentionrepost(file_list)
    mention_repost_dic = {'at': [33367121, 125878, 155265, 3229462, 539728, 1507827, 593637, 548927, 48481, 102277, 21420, 38591, 56575, 8484, 279392, 26166, 1719, 674], 'at_total': [50093531, 306495, 458379, 9057944, 1235165, 1572655, 1437399, 743510, 85103, 185246, 47384, 237729, 49800, 20252, 165925, 21466, 4662, 1385], 'repost': [20739153, 64585, 97812, 1627473, 326848, 1185745, 316554, 376596, 38987, 80730, 18386, 32595, 41406, 7101, 227952, 21175, 1376, 520], 'repost_total': [50093531, 306495, 458379, 9057944, 1235165, 1572655, 1437399, 743510, 85103, 185246, 47384, 237729, 49800, 20252, 165925, 21466, 4662, 1385]}


