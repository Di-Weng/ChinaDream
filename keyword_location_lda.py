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
    topic_sta1.keyword_lda(usingMongo = 0)
