# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2019-02-27 17:27
   Author  : diw
   Email   : di.W@hotmail.com
   File    : print_txt.py
   Desc: 由于G级的txt文件用sublime等软件打开会卡死，本代码旨在按行打印
-------------------------------
"""
from topic_sta1 import getLocation
current_file_path = '/Volumes/data/chinadream/data/201509.txt/201509.txt'

with open(current_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        line_section = line.split('\t')

        location = getLocation(line_section)
        print(location)
