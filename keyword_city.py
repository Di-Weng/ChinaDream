# _*_ coding:utf-8 _*_

'''

@author: diw

@contact: di.W@hotmail.com

@file: keyword_city

@time: 2018/10/23 16:39

@desc:

'''

import topic_sta1
weibofilefolder = '/Volumes/data/chinadream/data'

def store_data():
    file_path_list = topic_sta1.getAllFile(weibofilefolder)
    topic_sta1.collect_city_file(file_path_list)

def store_data_2():
    file_path_list = topic_sta1.getAllFile(weibofilefolder)
    topic_sta1.collect_emotion_city_file(file_path_list)
if __name__ == '__main__':

    # 不带情感
    # store_data()

    # 带情感
    store_data_2()

    #统计各keyword 和城市的微博语料数
    # topic_sta1.calc_city_doc()