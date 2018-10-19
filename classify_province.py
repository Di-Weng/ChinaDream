# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/10/17 18:56
   Author  : diw
   Email   : di.W@hotmail.com
   File    : classify_province.py
   Desc:
-------------------------------
"""

import topic_sta1
import pymongo
weibofilefolder = 'D:/chinadream/data'

if __name__ == '__main__':
    # document to MongoDB
    # file_path_list = topic_sta1.getAllFile(weibofilefolder)
    # topic_sta1.classify_Province(file_path_list)


    db = topic_sta1.conntoMongoWeiboProvince('192.168.12.120')


    provinceList = db.collection_names()

    for current_province in provinceList:
        current_collection = db[current_province]
        assert isinstance(current_collection, pymongo.collection.Collection)

        for current_mongodocument in current_collection.find().batch_size(300):
            print(current_mongodocument['location'])