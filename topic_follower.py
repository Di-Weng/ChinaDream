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
import pickle
from topic_sta1 import topic
weibofilefolder = 'D:/chinadream/data'



def process_statics():

    file_path_list = topic_sta1.getAllFile(weibofilefolder)
    topic_sta1.topic_followers(file_path_list)

if __name__ == '__main__':
    # process_statics()
    # 读取
    output_file = open('data/topic_follower.pickle', 'rb')
    output_dic = pickle.load(output_file)
    print(output_dic)

    echarts_list = []
    for followers_number, count_list in output_dic.items():
        for topic_count_index in range(len(count_list)):
            topic_count = count_list[topic_count_index]
            current_topic = topic[topic_count_index]
            temp = [followers_number,topic_count,current_topic]
            echarts_list.append(temp)
    print(echarts_list)

    output_file = open('result/follower_echarts.txt','w+',encoding = 'utf-8')
    output_file.write('[\n')
    max = len(echarts_list)
    count = 0
    for list_item in echarts_list:
        count += 1
        output_file.write(str(list_item))
        if(count < max):
            output_file.write(',\n')
        else:
            output_file.write('\n]')
    output_file.close()



