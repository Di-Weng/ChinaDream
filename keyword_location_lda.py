# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/10/22 20:00
   Author  : diw
   Email   : di.W@hotmail.com
   File    : keyword_location_lda.py
   Desc:
-------------------------------
"""
import topic_sta1

from gensim import models
from gensim.corpora import Dictionary
import codecs

if __name__=='__main__':
     #lda
     topic_sta1.keyword_location_lda()

     #输出结果
     topic_sta1.lda_city_topic()