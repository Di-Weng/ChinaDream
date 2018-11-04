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
weibofilefolder = '/Volumes/chinadream/data'



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
    print(output_dic)
    bash = 50
    new_output_dic = {}
    new_output_dic_per = {}
    new_output_dic['0'] = [0 for i in range(len(topic))]


    for follower_number_str, count_list in output_dic.items():
        bash_multiple = int(int(follower_number_str) / bash) + 1
        output_dic_index = bash_multiple * bash
        if(str(output_dic_index) not in new_output_dic.keys() and output_dic_index <= 100000):
            new_output_dic[str(output_dic_index)] = count_list
        elif(str(output_dic_index) in new_output_dic.keys() and output_dic_index <= 100000):
            original_list = new_output_dic[str(output_dic_index)]
            new_output_dic[str(output_dic_index)] = merge_list(original_list,count_list)
    for follower_label,count_list in new_output_dic.items():
        add_total = 0
        temp_count_list = []
        for count_temp in count_list:
            add_total += count_temp
        for j in range(len(count_list)):
            if(add_total == 0):
                temp_count_list.append(0)
            else:
                temp_count_list.append(float(count_list[j])/add_total)
        new_output_dic_per[follower_label] = temp_count_list


    echarts_list = []
    for followers_number, count_list in new_output_dic_per.items():
        for topic_count_index in range(len(count_list)):
            topic_count = count_list[topic_count_index]
            if(topic_count == 0):
                continue
            current_topic = topic[topic_count_index]
            temp = [followers_number,current_topic,topic_count]
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

    output_file = open('result/follower_echarts_multilines.txt', 'w+', encoding='utf-8')

    multiline_dic = {}
    for current_topic_temp in topic:
        multiline_dic[current_topic_temp] = []
    for x in output_list:
        temp_list = new_output_dic_per[x]
        for j in range(len(topic)):
            current_topic_temp = topic[j]
            multiline_dic[current_topic_temp].append(temp_list[j])
    for topic_temp, topic_list in multiline_dic.items():
        output_file.write(topic_temp)
        output_file.write('\n')
        output_file.write(str(topic_list))
        output_file.write('\n')
    output_file.close()
