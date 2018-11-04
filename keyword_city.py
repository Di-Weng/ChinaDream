# _*_ coding:utf-8 _*_

'''

@author: diw

@contact: di.W@hotmail.com

@file: keyword_city

@time: 2018/10/23 16:39

@desc:

'''

import topic_sta1
weibofilefolder = '/Volumes/chinadream/data'


if __name__ == '__main__':

    # file_path_list = topic_sta1.getAllFile(weibofilefolder)
    # topic_sta1.collect_city_file(file_path_list)

    #统计各keyword 和城市的微博语料数
    topic_sta1.calc_city_doc()