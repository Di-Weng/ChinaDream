# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/10/8 12:10
   Author  : diw
   Email   : di.W@hotmail.com
   File    : topic_keyword.py
   Desc:
-------------------------------
"""

from topic_sta1 import topic

from numba import jit


def get_echartsdata(input_dic):
    keyword_list = []
    series_dic = {}
    for keyword in input_dic.keys():
        keyword_list.append(keyword)
    for topic_label in topic:
        current_list = []
        index = topic.index(topic_label)
        for keyword in keyword_list:
            current_keyword_list = input_dic[keyword]
            if (index <= len(current_keyword_list) - 1):
                current_list.append(current_keyword_list[index])
            else:
                current_list.append(0)
        series_dic[topic_label] = current_list

    for series, series_list in series_dic.items():
        print(series)
        print(series_list)
        print('______________')
    # xAisx
    print(keyword_list)
    print(input_dic)
@jit
def calc_sum(topic_list):
    sum = 0
    for temp in topic_list:
        sum += temp
    return sum


def keyword_percent(calc_dic):
    output_dic = {}
    for keyword_current,current_list in calc_dic.items():
        output_dic[keyword_current] = []
        sum = calc_sum(current_list)
        temp_list = []
        for i in range(len(current_list)):
            temp_list.append(float(current_list[i])/sum)
        output_dic[keyword_current] = temp_list
    return output_dic

if __name__ == '__main__':
    topic_keyword = {'健康': [13367445, 4242206, 456251, 5131479, 18571447, 6040881, 128769],
                     '事业有成': [62028, 1086, 1582, 7419, 216058, 10843, 748],
                     '发展机会': [21737, 8738, 5659, 114518, 69272, 206817, 9837],
                     '生活幸福': [837976, 78089, 37532, 278012, 7072564, 522873, 46887],
                     '有房': [538488, 8349, 2605, 25187, 425761, 196021, 3069],
                     '出名': [519926, 84311, 32160, 127042, 632632, 80837, 23524],
                     '家庭幸福': [231345, 22258, 6799, 27263, 991264, 109216, 2310],
                     '好工作': [169169, 4037, 7744, 64306, 365524, 102102, 3365],
                     '平等机会': [8496, 3586, 1342, 18738, 22500, 19913, 696],
                     '白手起家': [29541, 3267, 978, 20486, 67899, 53472, 2702],
                     '成为富人': [14188, 2704, 160, 1517, 10860, 16047, 148],
                     '个体自由': [5944, 4651, 1489, 11029, 194719, 12362, 1619],
                     '安享晚年': [30594, 666, 696, 741, 9635, 2926, 1126],
                     '收入足够': [1476, 162, 244, 7737, 1963, 7378, 83],
                     '个人努力': [6908, 887, 1419, 14469, 121970, 16049, 945],
                     '祖国强大': [1443, 1238, 446, 332, 7068, 938, 7799],
                     '中国经济持续发展': [58, 41, 14, 38, 15, 4130, 77],
                     '父辈更好': [120, 10, 3, 157, 512, 492, 20]}
    percent_output = keyword_percent(topic_keyword)
    output = get_echartsdata(percent_output)
    temp_list = []
    for keyword_current,current_list in topic_keyword.items():
        temp_list.append(calc_sum(current_list))
    print(temp_list)