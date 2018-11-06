# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/11/4 下午11:07
   Author  : diw
   Email   : di.W@hotmail.com
   File    : keyword_emotion.py
   Desc:
-------------------------------
"""
import topic_sta1
from topic_sta1 import weibofilefolder
from topic_sta1 import keywords_list
from math import log
def get_result_dic():
    output_dic = {}
    file_path_list = topic_sta1.getAllFile(weibofilefolder)
    output_dic = topic_sta1.keyword_emotion(file_path_list)
    return output_dic

#log
def sum_all(iterable_object):
    sum = 0
    for temp in iterable_object.values():
        sum += log(temp)
    return sum

def sort_keyword_byallemotion(result_dic):
    output_dic = {}
    temp_dic = {}
    output_dic['keyword'] = []
    output_dic['log'] = []

    for current_keyword, current_keyword_list in result_dic.items():
        temp_dic[current_keyword] = sum_all(current_keyword_list)

    sorted_keyword_tuple = sorted(temp_dic.items(), key=lambda x: x[1], reverse=False)
    for current_tuple in sorted_keyword_tuple:
        output_dic['keyword'].append(current_tuple[0])
        output_dic['log'].append((current_tuple[1]))
    print(output_dic)
    return output_dic

def to_echartsData(result_dic, emotion_list, sorted_keywords_list):
    output_dic = {}
    # 对数量先进行排序

    for current_emotion in emotion_list:
        current_emotion_keywordList = []
        for current_keyword in sorted_keywords_list:
            current_keyword_emotionDic = result_dic[current_keyword]
            current_emotion_keywordList.append(log(current_keyword_emotionDic[current_emotion]))
        output_dic[current_emotion] = current_emotion_keywordList
    print(output_dic)
    return output_dic

def dismiss_unknowemotion(result_dic):
    output_dic = {}
    for keyword,tempdic in result_dic.items():
        output_dic[keyword] = {}
        for emotion,emotion_count in tempdic.items():
            if(emotion == '-1'):
                continue
            output_dic[keyword][emotion] = emotion_count
    return output_dic

if __name__=='__main__':
     #get result_dic
     # result_dic = get_result_dic()

     emotion_list = ['0','1','2','3','4']
     result_dic = {'健康': {'3': 10431113, '2': 26792199, '4': 2580746, '0': 4043353, '-1': 1177096, '1': 2913965}, '事业有成': {'2': 182625, '3': 93729, '-1': 2200, '0': 9446, '1': 10420, '4': 1338}, '发展机会': {'1': 35078, '2': 240583, '3': 25407, '4': 102948, '0': 30883, '-1': 1673}, '生活幸福': {'2': 5620765, '3': 2260554, '0': 107260, '1': 210780, '4': 598263, '-1': 76305}, '有房': {'2': 585255, '4': 23221, '0': 239103, '1': 88429, '3': 242650, '-1': 20816}, '出名': {'1': 179269, '0': 265398, '2': 779865, '-1': 45724, '3': 176544, '4': 53626}, '家庭幸福': {'0': 30577, '2': 898104, '1': 46120, '-1': 13928, '3': 334588, '4': 67132}, '好工作': {'2': 361045, '0': 61684, '1': 42414, '3': 224019, '-1': 10240, '4': 16839}, '平等机会': {'0': 6292, '2': 28517, '1': 13302, '3': 7778, '4': 18844, '-1': 532}, '白手起家': {'2': 99983, '1': 14435, '0': 6935, '4': 3537, '3': 51325, '-1': 2124}, '成为富人': {'0': 4720, '2': 27105, '4': 4514, '3': 6976, '1': 2062, '-1': 241}, '个体自由': {'4': 186214, '2': 13971, '-1': 499, '0': 2549, '3': 2767, '1': 25807}, '安享晚年': {'3': 22815, '0': 4039, '2': 13059, '1': 4846, '-1': 1116, '4': 503}, '收入足够': {'1': 2521, '2': 8989, '0': 2120, '3': 2275, '4': 3063, '-1': 69}, '个人努力': {'2': 59979, '3': 89586, '4': 6187, '-1': 794, '0': 1407, '1': 4688}, '祖国强大': {'2': 8334, '3': 5633, '0': 2391, '4': 1845, '1': 508, '-1': 547}, '中国经济持续发展': {'2': 2323, '4': 1208, '0': 470, '1': 308, '3': 47, '-1': 11}, '父辈更好': {'2': 571, '3': 234, '0': 142, '4': 329, '1': 28, '-1': 4}}
     result_dic = dismiss_unknowemotion(result_dic)
     sorted_keywords_dic = sort_keyword_byallemotion(result_dic)
     echarts_data = to_echartsData(result_dic,emotion_list,sorted_keywords_dic['keyword'])
