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
from numba import jit
weibofilefolder = 'D:/chinadream/data'



def process_statics():

    file_path_list = topic_sta1.getAllFile(weibofilefolder)
    topic_sta1.topic_followers(file_path_list)

@jit
def merge_list(list1,list2):
    temp_list = []
    for i in range(len(list1)):
        temp_list.append(list1[i] + list2[i])
    return temp_list

def sort_strlist(str_list):
    temp = {}
    for item in str_list:
        temp[item] = int(item)
    return sorted(str_list, key = lambda x:int(x))

if __name__ == '__main__':
    # process_statics()
    # 读取
    output_file = open('data/topic_follower.pickle', 'rb')
    output_dic = pickle.load(output_file)
    # print(output_dic)
    bash = 2000
    new_output_dic = {}
    new_output_dic['0'] = [0 for i in range(len(topic))]


    for follower_number_str, count_list in output_dic.items():
        bash_multiple = int(int(follower_number_str) / bash) + 1
        output_dic_index = bash_multiple * bash
        if(str(output_dic_index) not in new_output_dic.keys() and output_dic_index < 10000000):
            new_output_dic[str(output_dic_index)] = count_list
        elif(str(10000000) not in new_output_dic.keys() and output_dic_index >= 10000000):
            new_output_dic[str(10000000)] = count_list
        elif(str(output_dic_index) in new_output_dic.keys() and output_dic_index < 10000000):
            original_list = new_output_dic[str(output_dic_index)]
            new_output_dic[str(output_dic_index)] = merge_list(original_list,count_list)
        elif (str(10000000) in new_output_dic.keys() and output_dic_index >= 10000000):
            original_list = new_output_dic[str(10000000)]
            new_output_dic[str(10000000)] = merge_list(original_list, count_list)
    print(new_output_dic)

    echarts_list = []
    for followers_number, count_list in new_output_dic.items():
        for topic_count_index in range(len(count_list)):
            topic_count = count_list[topic_count_index]
            if(topic_count == 0):
                continue
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

    output_file = open('result/follower_echarts_xAxis.txt', 'w+', encoding='utf-8')
    out_list = list(new_output_dic.keys())
    output_list = sort_strlist(out_list)
    output_file.write(str(output_list))
    output_file.close()



