# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/10/14 19:39
   Author  : diw
   Email   : di.W@hotmail.com
   File    : keyword_coOccurrence.py
   Desc:
-------------------------------
"""

import topic_sta1
from topic_sta1 import keywords_list
import numpy as np
from numba import jit
weibofilefolder = 'D:/chinadream/data'
@jit
def list_sum(listA):
    sum = 0
    for temp in listA:
        sum += temp
    return sum

def get_result_dic(filefolder):
    file_path_list = topic_sta1.getAllFile(filefolder)
    result_dic = topic_sta1.keyword_coOccurrence(file_path_list)
    print(result_dic)

def to_gephi_edge_csv(input_dic):
    used_node_index = []
    node_id_dic = {}
    outfile = open('result/keyword_coOcurrence_nodes.csv','w+',encoding='utf-8')
    outfile.write('Id,Label,Modularity_Class,Value\n')
    temp_id = 0
    node_value_list = []
    for current_node, current_node_list in input_dic.items():
        node_value = list_sum(current_node_list)
        node_value_list.append(node_value)
        node_id_dic[current_node] = temp_id
        temp_id += 1

    print(node_value_list)

    node_value_max = np.max(node_value_list)
    node_value_min = np.min(node_value_list)

    modularity_list = []

    for current_node, current_node_list in input_dic.items():
        modularity_list.append(current_node)
        node_value = list_sum(current_node_list)
        node_std_value = float((node_value - node_value_min)) / (node_value_max - node_value_min)
        outfile.write(str(node_id_dic[current_node]))
        outfile.write(',')
        outfile.write(current_node)
        outfile.write(',')
        outfile.write(str(modularity_list.index(current_node)))
        outfile.write(',')
        outfile.write(str(node_value))
        outfile.write('\n')

    outfile.close()

    outfile = open('result/keyword_coOcurrence.csv', 'w+', encoding='utf-8')
    outfile.write('Source,Target,Weight,Type\n')

    coOccurence_list = []
    for current_count_list in input_dic.values():
        for current_count in current_count_list:
            coOccurence_list.append(current_count)
    total_coOccurence_max = np.max(coOccurence_list)
    total_coOccurence_min = np.min(coOccurence_list)

    for current_keyword, current_count_list in input_dic.items():
        used_node_index.append(keywords_list.index(current_keyword))

        for i in range(len(keywords_list)):
            if (i in used_node_index):
                continue
            temp = (current_keyword, keywords_list[i], current_count_list[i])
            if (current_count_list[i] == 0):
                continue
            current_weights = (current_count_list[i] / total_coOccurence_max) * 100
            outfile.write(str(node_id_dic[current_keyword]))
            outfile.write(',')
            outfile.write(str(node_id_dic[keywords_list[i]]))
            outfile.write(',')
            # outfile.write(str(current_count_list[i]))
            outfile.write(str(current_weights))
            outfile.write(',undirected')

            outfile.write('\n')
    outfile.close()
    print(modularity_list)


if __name__=='__main__':

    # # 1st_step
    # result_dic = get_result_dic(weibofilefolder)

    result_dic = {'健康': [0, 46580, 15803, 484402, 26795, 25229, 223910, 26597, 623, 660, 16928, 1717, 4965, 254, 342, 236, 613, 45], '事业有成': [46580, 0, 51, 10340, 9937, 206, 10539, 237, 1, 4368, 4, 4, 70, 2, 5, 2, 0, 0], '发展机会': [15803, 51, 0, 314, 131, 254, 108, 2767, 6315, 292, 31, 50, 3, 11, 43, 22, 28, 2], '生活幸福': [484402, 10340, 314, 0, 11652, 907, 270595, 6206, 103, 594, 81, 233, 609, 129, 248, 545, 4, 18], '有房': [26795, 9937, 131, 11652, 0, 223, 1048, 1086, 24, 214, 34, 16, 57, 99, 38, 8, 2, 1], '出名': [25229, 206, 254, 907, 223, 0, 270, 209, 22, 55, 13, 10, 17, 6, 14, 4, 2, 1], '家庭幸福': [223910, 10539, 108, 270595, 1048, 270, 0, 1007, 342, 699, 1317, 72, 288, 382, 96, 50, 2, 1], '好工作': [26597, 237, 2767, 6206, 1086, 209, 1007, 0, 23, 27, 13, 10, 57, 31, 22, 5, 0, 2], '平等机会': [623, 1, 6315, 103, 24, 22, 342, 23, 0, 21, 29, 55, 4, 94, 27, 0, 0, 0], '白手起家': [660, 4368, 292, 594, 214, 55, 699, 27, 21, 0, 33, 128, 7, 25, 38, 0, 0, 3], '成为富人': [16928, 4, 31, 81, 34, 13, 1317, 13, 29, 33, 0, 1, 29, 5, 6, 0, 0, 0], '个体自由': [1717, 4, 50, 233, 16, 10, 72, 10, 55, 128, 1, 0, 0, 2, 12, 0, 0, 0], '安享晚年': [4965, 70, 3, 609, 57, 17, 288, 57, 4, 7, 29, 0, 0, 3, 0, 3, 0, 0], '收入足够': [254, 2, 11, 129, 99, 6, 382, 31, 94, 25, 5, 2, 3, 0, 1, 0, 0, 0], '个人努力': [342, 5, 43, 248, 38, 14, 96, 22, 27, 38, 6, 12, 0, 1, 0, 21, 0, 0], '祖国强大': [236, 2, 22, 545, 8, 4, 50, 5, 0, 0, 0, 0, 3, 0, 21, 0, 0, 0], '中国经济持续发展': [613, 0, 28, 4, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '父辈更好': [45, 0, 2, 18, 1, 1, 1, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0]}
    to_gephi_edge_csv(result_dic)
