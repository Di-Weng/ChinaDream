# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/11/6 10:25
   Author  : diw
   Email   : di.W@hotmail.com
   File    : keyword_emotion_time.py
   Desc:
-------------------------------
"""
import topic_sta1
from topic_sta1 import keywords_list
from math import log

emotion_list = ['0', '1', '2', '3', '4']

def get_data():
    file_path_list = topic_sta1.getAllFile(topic_sta1.weibofilefolder)
    # 输出结果
    topic_sta1.keyword_emotion_time(file_path_list)

#log
def sum_all(iterable_object,isLog = 0):
    sum = 0
    if(isLog):
        for temp in iterable_object.values():
            sum += log(temp)
    else:
        for temp in iterable_object.values():
            sum += temp
    return sum

def echarts_output(input_dic,emotion_list):

    output_dic = {}
    for current_emotion in emotion_list:
        output_dic[current_emotion] = {}
        for current_time, time_dic in input_dic.items():
            current_emotion_keywordList = []
            for current_keyword in keywords_list:
                current_keyword_emotionDic = time_dic[current_keyword]
                if(current_emotion in current_keyword_emotionDic.keys()):
                    current_emotion_keywordList.append(current_keyword_emotionDic[current_emotion])
                else:
                    current_emotion_keywordList.append(0)
            output_dic[current_emotion][current_time] = current_emotion_keywordList

    for i in range(len(emotion_list)):
        current_emotion = emotion_list[i]
        print()
        print(current_emotion)
        for current_time,keyword_emotion_list in output_dic[current_emotion].items():
            print('\''+ current_time + '\':',end='')
            print(keyword_emotion_list,end=',\n')
    return output_dic

def dismiss_unknowemotion(result_dic):
    output_dic = {}
    for current_time,current_time_dic in result_dic.items():
        output_dic[current_time] = {}
        for keyword,tempdic in current_time_dic.items():
            output_dic[current_time][keyword] = {}
            for emotion,emotion_count in tempdic.items():
                if(emotion == '-1'):
                    continue
                output_dic[current_time][keyword][emotion] = emotion_count
    return output_dic

def get_timeList(input_dic):
    output_list = []
    for current_time in input_dic.keys():
        output_list.append(current_time)
    output_list_sorted = sorted(output_list,reverse=False)
    print(output_list_sorted)

    return output_list_sorted

#test only
def keyword_stdouput():
    for current_emotion in emotion_list:
        out_str = '{name: \'' + current_emotion + '\', type: \'bar\',stack:\'总量\'},'
        print(out_str)

#test only
def option_stdoutput(time_list):
    for current_time in time_list:
        print('        {')
        print('            title: {text: \''+ current_time + '\'},')
        print('            series: [')
        for i in range(len(emotion_list)):
            print('                {data: dataMap.data' + str(i) +'[\''+ current_time + '\']},')
        print('            ]')
        print('        },')

def trans_result2Percent(input_data):
    output_dic = {}
    for current_time,current_time_list in input_data.items():
        output_dic[current_time] = {}
        for current_keyword, current_keyword_dic in current_time_list.items():
            output_dic[current_time][current_keyword] = {}
            sum = sum_all(current_keyword_dic)
            for current_keyword_emotion, emotion_count in current_keyword_dic.items():
                output_dic[current_time][current_keyword][current_keyword_emotion] = float(emotion_count) / sum

    return output_dic

if __name__ == '__main__':
    #get result_data
    # result_data = get_data()

    result_dic = {'201409': {'健康': {'3': 164364, '2': 450143, '4': 39723, '0': 86500, '-1': 41619, '1': 59434}, '事业有成': {'2': 2602, '3': 1106, '-1': 48, '0': 285, '1': 130, '4': 20}, '发展机会': {'1': 901, '2': 5168, '3': 421, '4': 942, '0': 529, '-1': 92}, '生活幸福': {'2': 77154, '3': 31519, '0': 1705, '1': 2091, '4': 8494, '-1': 2493}, '有房': {'2': 9285, '4': 655, '0': 4938, '1': 1500, '3': 4061, '-1': 687}, '出名': {'1': 3209, '0': 5722, '2': 13026, '-1': 1735, '3': 2360, '4': 755}, '家庭幸福': {'0': 1133, '2': 12883, '1': 410, '-1': 737, '3': 4867, '4': 839}, '好工作': {'2': 5407, '0': 1260, '1': 801, '3': 3249, '-1': 323, '4': 266}, '平等机会': {'0': 465, '2': 830, '1': 95, '3': 52, '4': 154, '-1': 20}, '白手起家': {'2': 2370, '1': 327, '0': 208, '4': 52, '3': 624, '-1': 287}, '成为富人': {'0': 106, '2': 541, '4': 120, '3': 177, '1': 87, '-1': 27}, '个体自由': {'4': 8278, '2': 627, '-1': 26, '0': 55, '3': 54, '1': 108}, '安享晚年': {'3': 1215, '0': 108, '2': 118, '1': 65, '-1': 42, '4': 17}, '收入足够': {'1': 15, '2': 93, '0': 44, '3': 26, '4': 7, '-1': 4}, '个人努力': {'2': 230, '3': 652, '4': 84, '-1': 23, '0': 10, '1': 114}, '祖国强大': {'2': 69, '3': 55, '0': 35, '4': 35, '1': 3, '-1': 8}, '中国经济持续发展': {'2': 171, '4': 62, '0': 3, '1': 0, '3': 0}, '父辈更好': {'2': 5, '3': 4, '0': 3, '4': 5}}, '201410': {'健康': {'2': 1417936, '1': 155617, '4': 123607, '3': 484102, '-1': 126070, '0': 249749}, '事业有成': {'3': 3522, '2': 7995, '0': 295, '-1': 118, '1': 399, '4': 48}, '发展机会': {'1': 1653, '2': 9006, '4': 1716, '3': 1111, '-1': 407, '0': 864}, '生活幸福': {'2': 546373, '3': 203313, '0': 3880, '4': 43364, '1': 9129, '-1': 10854}, '有房': {'3': 13094, '2': 38347, '1': 2922, '0': 11185, '-1': 1634, '4': 805}, '出名': {'2': 31874, '0': 11687, '1': 5790, '-1': 3762, '3': 4791, '4': 1545}, '家庭幸福': {'3': 15311, '4': 2068, '2': 44213, '-1': 1167, '1': 1498, '0': 1584}, '好工作': {'2': 15856, '3': 10720, '4': 352, '1': 3794, '-1': 1081, '0': 2231}, '平等机会': {'0': 241, '2': 1070, '4': 474, '1': 572, '3': 194, '-1': 67}, '白手起家': {'2': 5638, '3': 3078, '1': 819, '-1': 635, '0': 228, '4': 99}, '成为富人': {'2': 2010, '3': 350, '4': 222, '0': 183, '1': 96, '-1': 25}, '个体自由': {'1': 531, '0': 82, '4': 12339, '2': 337, '3': 68, '-1': 36}, '安享晚年': {'3': 1001, '1': 169, '2': 179, '0': 163, '-1': 73, '4': 32}, '收入足够': {'2': 295, '0': 110, '3': 68, '4': 73, '1': 47, '-1': 11}, '个人努力': {'3': 2192, '2': 878, '4': 144, '0': 39, '1': 91, '-1': 39}, '祖国强大': {'2': 229, '-1': 39, '3': 106, '4': 47, '0': 56, '1': 13}, '中国经济持续发展': {'2': 468, '4': 70, '0': 15, '1': 7, '-1': 1}, '父辈更好': {'3': 6, '1': 1, '2': 215, '0': 1, '4': 6}}, '201411': {'健康': {'2': 782256, '0': 212764, '1': 89864, '3': 293907, '-1': 85515, '4': 63924}, '事业有成': {'3': 3535, '1': 198, '2': 5175, '0': 218, '-1': 112, '4': 97}, '发展机会': {'0': 785, '2': 6897, '-1': 250, '4': 1262, '1': 1446, '3': 914}, '生活幸福': {'-1': 5158, '2': 175202, '3': 70283, '4': 13323, '1': 3616, '0': 2709}, '有房': {'2': 13067, '3': 9942, '0': 5835, '1': 2016, '-1': 739, '4': 714}, '出名': {'0': 6569, '2': 18531, '1': 4206, '3': 4085, '-1': 4127, '4': 1096}, '家庭幸福': {'2': 21944, '0': 965, '3': 11682, '4': 1116, '1': 837, '-1': 850}, '好工作': {'3': 6268, '1': 1369, '2': 9002, '0': 2293, '-1': 646, '4': 279}, '平等机会': {'1': 1059, '4': 300, '2': 1444, '3': 290, '0': 201, '-1': 178}, '白手起家': {'2': 3246, '1': 274, '0': 190, '3': 504, '-1': 88, '4': 59}, '成为富人': {'2': 1316, '0': 106, '4': 152, '3': 363, '1': 83, '-1': 33}, '个体自由': {'4': 2928, '0': 86, '2': 228, '1': 67, '-1': 56, '3': 45}, '安享晚年': {'1': 156, '3': 594, '2': 160, '0': 89, '-1': 38, '4': 6}, '收入足够': {'-1': 8, '0': 53, '4': 91, '2': 237, '1': 33, '3': 76}, '个人努力': {'2': 668, '3': 809, '4': 110, '1': 152, '0': 55, '-1': 127}, '祖国强大': {'0': 45, '2': 220, '4': 25, '3': 128, '-1': 58, '1': 6}, '中国经济持续发展': {'2': 139, '0': 17, '4': 47, '-1': 0, '1': 3, '3': 0}, '父辈更好': {'2': 15, '4': 7, '3': 4, '0': 0, '1': 1, '-1': 1}}, '201412': {'健康': {'3': 376532, '2': 1136468, '-1': 109079, '1': 111092, '0': 142498, '4': 87592}, '事业有成': {'2': 6648, '3': 3317, '-1': 269, '0': 418, '4': 93, '1': 275}, '发展机会': {'2': 7643, '1': 1633, '3': 857, '4': 1877, '0': 784, '-1': 180}, '生活幸福': {'3': 80540, '2': 185672, '4': 15677, '0': 4236, '-1': 6484, '1': 4405}, '有房': {'3': 7620, '2': 14630, '0': 7724, '1': 2498, '-1': 1091, '4': 1059}, '出名': {'2': 23676, '0': 10124, '3': 5130, '-1': 4296, '1': 6508, '4': 1744}, '家庭幸福': {'2': 32987, '3': 13319, '-1': 1321, '1': 1108, '4': 1931, '0': 1544}, '好工作': {'3': 8878, '2': 14561, '1': 1762, '0': 2258, '-1': 1146, '4': 362}, '平等机会': {'4': 549, '1': 1129, '3': 211, '-1': 78, '2': 819, '0': 245}, '白手起家': {'2': 4358, '3': 585, '1': 363, '0': 116, '-1': 126, '4': 86}, '成为富人': {'3': 260, '1': 66, '2': 1433, '0': 163, '4': 138, '-1': 87}, '个体自由': {'4': 2552, '1': 122, '-1': 71, '0': 90, '2': 226, '3': 53}, '安享晚年': {'3': 933, '2': 229, '0': 223, '1': 280, '-1': 147, '4': 24}, '收入足够': {'2': 222, '4': 61, '0': 54, '3': 69, '1': 46, '-1': 12}, '个人努力': {'3': 1203, '2': 715, '4': 120, '-1': 128, '0': 41, '1': 243}, '祖国强大': {'2': 149, '0': 51, '4': 45, '3': 207, '-1': 29, '1': 9}, '中国经济持续发展': {'2': 161, '4': 85, '0': 50, '1': 6, '-1': 3, '3': 0}, '父辈更好': {'3': 6, '4': 5, '2': 47, '0': 9}}, '201501': {'健康': {'2': 1271165, '3': 449390, '-1': 108943, '1': 122246, '4': 100159, '0': 165171}, '事业有成': {'3': 4360, '2': 9435, '-1': 368, '1': 513, '0': 407, '4': 112}, '发展机会': {'2': 9510, '3': 864, '4': 2509, '1': 1897, '0': 1095, '-1': 261}, '生活幸福': {'3': 90500, '2': 219971, '1': 5903, '4': 19865, '0': 4597, '-1': 5811}, '有房': {'2': 20683, '3': 9270, '1': 3102, '0': 9866, '-1': 1402, '4': 909}, '出名': {'2': 30185, '1': 9643, '-1': 6196, '3': 7746, '0': 14962, '4': 2005}, '家庭幸福': {'3': 16354, '2': 40749, '-1': 1408, '4': 1726, '0': 1340, '1': 1723}, '好工作': {'2': 17098, '3': 10413, '-1': 1475, '1': 1934, '0': 3036, '4': 546}, '平等机会': {'3': 191, '2': 738, '4': 2895, '1': 3048, '0': 342, '-1': 39}, '白手起家': {'2': 6191, '3': 649, '0': 224, '1': 991, '4': 614, '-1': 444}, '成为富人': {'3': 244, '2': 1395, '4': 231, '0': 188, '1': 78, '-1': 27}, '个体自由': {'2': 346, '4': 5554, '1': 749, '3': 85, '0': 119, '-1': 84}, '安享晚年': {'3': 829, '2': 357, '-1': 427, '1': 378, '0': 267, '4': 68}, '收入足够': {'2': 256, '4': 112, '1': 66, '3': 114, '0': 76, '-1': 12}, '个人努力': {'3': 1424, '2': 813, '-1': 73, '0': 78, '4': 138, '1': 169}, '祖国强大': {'2': 127, '3': 102, '4': 34, '0': 36, '-1': 38, '1': 4}, '中国经济持续发展': {'2': 99, '0': 13, '4': 62, '3': 2, '1': 6, '-1': 2}, '父辈更好': {'2': 17, '0': 22, '1': 1, '3': 6, '4': 4}}, '201502': {'健康': {'2': 1295112, '3': 462336, '1': 148872, '0': 201298, '-1': 49622, '4': 119294}, '事业有成': {'2': 14313, '1': 703, '3': 5324, '0': 400, '-1': 162, '4': 146}, '发展机会': {'1': 2277, '2': 12412, '3': 1040, '4': 4851, '0': 1915, '-1': 31}, '生活幸福': {'2': 238818, '3': 92553, '1': 11143, '0': 4909, '4': 20795, '-1': 2732}, '有房': {'2': 25250, '3': 11759, '0': 12058, '-1': 801, '1': 4923, '4': 1393}, '出名': {'0': 14649, '-1': 1129, '1': 10718, '2': 35552, '3': 8570, '4': 2441}, '家庭幸福': {'2': 54809, '3': 16141, '1': 2867, '4': 2861, '0': 1706, '-1': 1026}, '好工作': {'1': 1450, '2': 16638, '3': 8990, '0': 2480, '-1': 1204, '4': 798}, '平等机会': {'1': 636, '4': 2839, '2': 895, '0': 217, '3': 299, '-1': 16}, '白手起家': {'2': 4670, '3': 1034, '1': 1236, '0': 217, '-1': 49, '4': 209}, '成为富人': {'3': 175, '2': 1594, '1': 120, '4': 226, '-1': 7, '0': 265}, '个体自由': {'0': 126, '4': 6257, '2': 332, '1': 900, '-1': 16, '3': 70}, '安享晚年': {'2': 268, '3': 790, '0': 357, '1': 197, '-1': 13, '4': 10}, '收入足够': {'2': 381, '4': 185, '3': 37, '0': 59, '1': 82, '-1': 0}, '个人努力': {'3': 1359, '1': 145, '2': 948, '4': 230, '0': 42, '-1': 18}, '祖国强大': {'2': 161, '4': 46, '3': 61, '0': 39, '1': 7, '-1': 6}, '中国经济持续发展': {'2': 140, '4': 91, '0': 9, '1': 2}, '父辈更好': {'0': 74, '2': 20, '4': 5, '3': 7, '1': 0}}, '201503': {'健康': {'0': 185212, '2': 1010701, '3': 358742, '4': 106308, '1': 138784, '-1': 21887}, '事业有成': {'3': 4567, '2': 9456, '4': 24, '1': 494, '0': 330, '-1': 28}, '发展机会': {'4': 4391, '1': 2018, '2': 12009, '0': 1802, '3': 1166, '-1': 24}, '生活幸福': {'2': 240179, '3': 88211, '1': 9113, '4': 21522, '0': 5743, '-1': 1385}, '有房': {'2': 24620, '3': 10462, '1': 4038, '4': 1177, '0': 12652, '-1': 894}, '出名': {'0': 12885, '2': 30432, '4': 1946, '3': 7497, '1': 7675, '-1': 1127}, '家庭幸福': {'2': 37485, '3': 13376, '4': 2799, '1': 2990, '-1': 247, '0': 1581}, '好工作': {'2': 15346, '3': 7432, '0': 2462, '1': 1419, '4': 679, '-1': 201}, '平等机会': {'4': 697, '0': 340, '2': 1255, '3': 359, '1': 1070, '-1': 4}, '白手起家': {'2': 7632, '3': 2121, '4': 126, '1': 1734, '0': 196, '-1': 24}, '成为富人': {'4': 193, '2': 998, '0': 188, '3': 148, '1': 112}, '个体自由': {'4': 5223, '1': 1170, '2': 408, '0': 151, '3': 70, '-1': 9}, '安享晚年': {'3': 759, '0': 333, '1': 157, '2': 254, '-1': 9, '4': 2}, '收入足够': {'1': 134, '4': 158, '2': 621, '0': 110, '3': 56, '-1': 1}, '个人努力': {'4': 189, '3': 1071, '1': 567, '2': 938, '0': 47, '-1': 12}, '祖国强大': {'0': 37, '4': 101, '2': 146, '3': 130, '1': 12, '-1': 8}, '中国经济持续发展': {'4': 37, '0': 5, '3': 1, '2': 117, '1': 4}, '父辈更好': {'2': 28, '4': 2, '3': 6, '1': 1, '0': 0}}, '201504': {'健康': {'2': 943745, '3': 385769, '1': 120275, '4': 98049, '0': 135367, '-1': 36952}, '事业有成': {'2': 9232, '3': 4381, '1': 413, '0': 652, '-1': 24, '4': 22}, '发展机会': {'2': 9958, '1': 1547, '3': 1211, '4': 5463, '0': 1011, '-1': 16}, '生活幸福': {'3': 92556, '2': 208309, '4': 24778, '1': 6557, '-1': 2082, '0': 4223}, '有房': {'2': 22181, '3': 10734, '1': 4048, '0': 8500, '-1': 766, '4': 582}, '出名': {'2': 27377, '3': 7264, '0': 11327, '1': 7031, '-1': 1276, '4': 2125}, '家庭幸福': {'3': 12582, '2': 33385, '4': 2655, '1': 2179, '-1': 193, '0': 932}, '好工作': {'3': 7913, '2': 14316, '0': 2546, '4': 725, '1': 1778, '-1': 239}, '平等机会': {'4': 639, '1': 720, '2': 837, '0': 145, '3': 369, '-1': 3}, '白手起家': {'1': 814, '3': 2793, '2': 7680, '4': 215, '0': 136, '-1': 32}, '成为富人': {'2': 1461, '1': 46, '4': 135, '3': 232, '0': 63}, '个体自由': {'4': 4967, '1': 1340, '3': 65, '2': 538, '0': 106, '-1': 6}, '安享晚年': {'3': 781, '2': 262, '0': 97, '1': 98, '-1': 9, '4': 5}, '收入足够': {'3': 48, '2': 885, '4': 173, '1': 111, '0': 51}, '个人努力': {'3': 1376, '4': 122, '2': 1664, '0': 84, '-1': 10, '1': 202}, '祖国强大': {'2': 291, '4': 149, '1': 11, '3': 417, '0': 100, '-1': 30}, '中国经济持续发展': {'4': 34, '2': 65, '0': 3, '1': 2, '3': 0}, '父辈更好': {'4': 3, '3': 11, '2': 13, '0': 0}}, '201505': {'健康': {'3': 495313, '2': 1352423, '0': 160368, '1': 138220, '4': 115862, '-1': 51965}, '事业有成': {'2': 12496, '3': 4064, '-1': 29, '1': 342, '0': 466, '4': 27}, '发展机会': {'0': 1052, '4': 5948, '1': 1831, '2': 17322, '3': 1405, '-1': 14}, '生活幸福': {'2': 239414, '1': 5987, '3': 99265, '4': 23938, '0': 4070, '-1': 1870}, '有房': {'2': 31587, '0': 9089, '3': 11944, '1': 3823, '4': 650, '-1': 580}, '出名': {'2': 32031, '0': 13195, '4': 2179, '1': 7835, '3': 8300, '-1': 1293}, '家庭幸福': {'2': 38111, '3': 14708, '4': 3589, '1': 2616, '0': 1108, '-1': 300}, '好工作': {'2': 16417, '3': 9157, '1': 1564, '0': 2796, '4': 950, '-1': 226}, '平等机会': {'1': 630, '4': 723, '2': 1028, '3': 353, '0': 122, '-1': 5}, '白手起家': {'2': 3668, '3': 5744, '0': 136, '1': 455, '4': 180, '-1': 51}, '成为富人': {'2': 1329, '3': 348, '0': 84, '4': 182, '1': 41}, '个体自由': {'4': 10193, '1': 1438, '3': 81, '2': 451, '-1': 8, '0': 89}, '安享晚年': {'2': 259, '3': 759, '0': 68, '1': 125, '4': 21, '-1': 7}, '收入足够': {'2': 327, '4': 158, '1': 36, '0': 46, '3': 67}, '个人努力': {'2': 1395, '3': 1616, '4': 150, '-1': 15, '0': 44, '1': 162}, '祖国强大': {'2': 216, '3': 113, '4': 35, '0': 64, '-1': 4, '1': 7}, '中国经济持续发展': {'2': 42, '1': 6, '0': 8, '4': 44, '-1': 0}, '父辈更好': {'2': 10, '3': 15, '0': 0, '4': 12}}, '201506': {'健康': {'2': 1064247, '1': 109103, '3': 424888, '0': 148310, '4': 110960, '-1': 41876}, '事业有成': {'3': 3612, '2': 9940, '1': 332, '0': 257, '4': 24, '-1': 192}, '发展机会': {'1': 1034, '2': 9781, '4': 5136, '0': 1156, '3': 1069, '-1': 14}, '生活幸福': {'2': 192170, '4': 21233, '3': 85140, '1': 4831, '0': 3396, '-1': 1625}, '有房': {'2': 23259, '3': 9774, '0': 8314, '1': 3226, '4': 620, '-1': 579}, '出名': {'2': 30208, '3': 6999, '0': 13387, '1': 7543, '4': 2887, '-1': 1336}, '家庭幸福': {'3': 14730, '2': 32142, '4': 3116, '0': 1367, '1': 2039, '-1': 223}, '好工作': {'2': 12870, '1': 1321, '3': 7683, '0': 2300, '4': 839, '-1': 227}, '平等机会': {'1': 312, '4': 605, '2': 842, '3': 339, '0': 132, '-1': 6}, '白手起家': {'2': 2935, '3': 3794, '1': 308, '4': 142, '0': 93, '-1': 22}, '成为富人': {'2': 978, '4': 210, '3': 235, '0': 47, '1': 34}, '个体自由': {'1': 1450, '4': 7568, '2': 466, '3': 845, '0': 187, '-1': 16}, '安享晚年': {'3': 925, '0': 80, '2': 197, '1': 176, '4': 22, '-1': 16}, '收入足够': {'2': 297, '0': 44, '4': 167, '1': 26, '3': 48}, '个人努力': {'2': 1255, '0': 40, '3': 1600, '4': 125, '1': 138, '-1': 30}, '祖国强大': {'2': 207, '4': 39, '3': 47, '0': 44, '-1': 3, '1': 4}, '中国经济持续发展': {'2': 23, '4': 17, '3': 3, '0': 1}, '父辈更好': {'2': 17, '3': 10, '4': 2, '1': 3, '0': 2}}, '201507': {'健康': {'2': 784536, '3': 344295, '-1': 39468, '0': 125143, '1': 93516, '4': 98182}, '事业有成': {'3': 3508, '2': 4748, '-1': 78, '1': 173, '0': 255, '4': 40}, '发展机会': {'2': 8933, '1': 998, '4': 5452, '0': 1030, '3': 1006, '-1': 17}, '生活幸福': {'3': 70378, '2': 167108, '4': 16606, '-1': 1446, '0': 3658, '1': 4714}, '有房': {'2': 15970, '3': 7347, '4': 530, '0': 7312, '-1': 457, '1': 3068}, '出名': {'-1': 1277, '3': 6800, '2': 29781, '1': 7524, '0': 10704, '4': 2081}, '家庭幸福': {'3': 10682, '2': 24124, '0': 885, '1': 1778, '4': 2906, '-1': 264}, '好工作': {'2': 12809, '3': 9794, '0': 2528, '4': 1011, '1': 1396, '-1': 241}, '平等机会': {'3': 315, '2': 815, '4': 645, '0': 89, '1': 152, '-1': 5}, '白手起家': {'2': 2286, '3': 1741, '4': 195, '0': 115, '1': 293, '-1': 17}, '成为富人': {'2': 941, '3': 288, '4': 201, '1': 35, '0': 54, '-1': 2}, '个体自由': {'3': 76, '4': 4987, '1': 1016, '0': 118, '2': 443, '-1': 4}, '安享晚年': {'3': 715, '0': 65, '2': 216, '1': 90, '4': 12, '-1': 22}, '收入足够': {'4': 177, '2': 302, '3': 65, '0': 32, '1': 47}, '个人努力': {'2': 1375, '3': 953, '-1': 35, '4': 197, '1': 114, '0': 27}, '祖国强大': {'2': 212, '3': 71, '-1': 4, '0': 43, '4': 41, '1': 9}, '中国经济持续发展': {'2': 14, '4': 23, '0': 9}, '父辈更好': {'2': 8, '0': 0, '3': 6, '4': 2, '1': 0}}, '201508': {'健康': {'1': 154112, '3': 559693, '2': 1338988, '4': 175310, '-1': 29414, '0': 216553}, '事业有成': {'2': 8320, '3': 6988, '0': 505, '1': 732, '-1': 63, '4': 25}, '发展机会': {'2': 18997, '1': 2075, '4': 9993, '0': 1862, '3': 2173, '-1': 14}, '生活幸福': {'2': 298573, '3': 112402, '-1': 3217, '4': 33425, '1': 13461, '0': 6332}, '有房': {'2': 24261, '3': 10636, '0': 12915, '1': 5286, '4': 769, '-1': 827}, '出名': {'3': 12694, '2': 52816, '1': 12064, '0': 14883, '4': 4068, '-1': 1558}, '家庭幸福': {'3': 16368, '2': 42149, '-1': 404, '1': 2528, '4': 6342, '0': 1423}, '好工作': {'3': 8834, '2': 18832, '4': 2157, '0': 3791, '1': 1979, '-1': 168}, '平等机会': {'4': 1284, '2': 1879, '1': 275, '3': 577, '0': 176, '-1': 0}, '白手起家': {'2': 4481, '3': 4845, '4': 305, '1': 701, '0': 380, '-1': 22}, '成为富人': {'3': 543, '2': 1891, '4': 346, '0': 78, '1': 252}, '个体自由': {'4': 7466, '2': 739, '1': 1260, '0': 72, '-1': 5, '3': 112}, '安享晚年': {'3': 1096, '2': 676, '1': 192, '0': 156, '-1': 23, '4': 12}, '收入足够': {'2': 488, '4': 448, '0': 66, '3': 71, '1': 24}, '个人努力': {'2': 1647, '3': 1145, '4': 160, '1': 238, '-1': 20, '0': 59}, '祖国强大': {'2': 446, '0': 91, '3': 396, '-1': 26, '4': 64, '1': 9}, '中国经济持续发展': {'4': 36, '2': 355, '0': 7, '1': 2}, '父辈更好': {'3': 10, '4': 6, '2': 11, '0': 0}}, '201509': {'健康': {'2': 1159146, '3': 475247, '0': 177388, '1': 123761, '4': 128318, '-1': 31050}, '事业有成': {'1': 718, '2': 6904, '3': 5620, '0': 391, '-1': 28, '4': 12}, '发展机会': {'4': 7744, '1': 1847, '3': 1680, '2': 14446, '0': 1238, '-1': 12}, '生活幸福': {'4': 31346, '2': 264518, '3': 107487, '-1': 2312, '1': 10759, '0': 4991}, '有房': {'3': 9556, '0': 9569, '2': 24584, '1': 4106, '-1': 759, '4': 825}, '出名': {'1': 8332, '3': 7069, '2': 38386, '4': 3031, '0': 11276, '-1': 1214}, '家庭幸福': {'2': 41115, '3': 14371, '4': 4149, '1': 2549, '0': 882, '-1': 576}, '好工作': {'3': 7560, '2': 16701, '1': 1580, '0': 3012, '4': 1363, '-1': 303}, '平等机会': {'2': 1667, '4': 832, '1': 236, '3': 393, '0': 113, '-1': 3}, '白手起家': {'2': 4417, '3': 3031, '1': 485, '4': 346, '0': 178, '-1': 29}, '成为富人': {'2': 1223, '1': 188, '4': 268, '3': 382, '0': 158}, '个体自由': {'4': 8799, '2': 545, '1': 1208, '3': 73, '0': 130, '-1': 9}, '安享晚年': {'3': 1093, '2': 333, '1': 183, '0': 73, '-1': 43, '4': 11}, '收入足够': {'4': 269, '2': 526, '3': 36, '0': 43, '1': 49}, '个人努力': {'3': 1309, '2': 1773, '4': 165, '1': 112, '-1': 26, '0': 82}, '祖国强大': {'0': 255, '2': 829, '3': 1414, '4': 215, '1': 95, '-1': 90}, '中国经济持续发展': {'2': 137, '0': 19, '4': 27, '3': 1}, '父辈更好': {'3': 11, '2': 5, '4': 3}}, '201510': {'健康': {'3': 419294, '2': 1112658, '4': 104512, '0': 152015, '1': 113233, '-1': 30338}, '事业有成': {'3': 4325, '1': 443, '2': 6260, '0': 337, '-1': 29, '4': 22}, '发展机会': {'4': 5271, '2': 10125, '3': 1618, '1': 1305, '0': 1119, '-1': 23}, '生活幸福': {'2': 243146, '3': 94554, '0': 5897, '4': 35848, '-1': 3391, '1': 8403}, '有房': {'2': 35887, '0': 10270, '3': 8351, '1': 3754, '4': 1673, '-1': 745}, '出名': {'2': 36169, '4': 2383, '0': 12572, '1': 6856, '3': 6851, '-1': 1433}, '家庭幸福': {'3': 12600, '2': 40340, '4': 2174, '1': 2667, '0': 1000, '-1': 378}, '好工作': {'2': 13603, '3': 7025, '4': 1010, '0': 2425, '1': 1357, '-1': 183}, '平等机会': {'2': 994, '4': 654, '0': 214, '1': 283, '3': 309, '-1': 12}, '白手起家': {'2': 3445, '0': 90, '3': 1543, '4': 191, '1': 480, '-1': 27}, '成为富人': {'2': 1044, '3': 352, '1': 175, '0': 112, '4': 174}, '个体自由': {'4': 17886, '2': 487, '0': 73, '1': 1040, '3': 65, '-1': 1}, '安享晚年': {'1': 195, '3': 1074, '2': 272, '0': 105, '-1': 27, '4': 41}, '收入足够': {'4': 70, '3': 80, '2': 118, '1': 36, '0': 63, '-1': 0}, '个人努力': {'3': 1347, '2': 1599, '4': 143, '-1': 21, '1': 114, '0': 31}, '祖国强大': {'2': 472, '3': 179, '0': 71, '-1': 19, '4': 29, '1': 6}, '中国经济持续发展': {'4': 52, '0': 12, '3': 1, '2': 27, '1': 1}, '父辈更好': {'3': 11, '2': 13, '1': 0, '4': 3, '0': 4}}, '201511': {'健康': {'3': 477420, '2': 1133415, '4': 104700, '1': 128737, '0': 153334, '-1': 36443}, '事业有成': {'2': 7190, '3': 4157, '0': 526, '1': 633, '-1': 36, '4': 32}, '发展机会': {'4': 3412, '0': 738, '2': 8791, '1': 1458, '3': 903, '-1': 25}, '生活幸福': {'2': 268700, '4': 36793, '1': 7610, '3': 110405, '-1': 6126, '0': 4083}, '有房': {'0': 9765, '3': 9711, '2': 42447, '1': 3379, '-1': 766, '4': 534}, '出名': {'2': 30607, '3': 6665, '-1': 1359, '1': 5495, '0': 9526, '4': 2005}, '家庭幸福': {'2': 34618, '3': 14865, '0': 1127, '4': 2356, '1': 2342, '-1': 378}, '好工作': {'0': 2302, '2': 16873, '1': 1747, '3': 8510, '4': 686, '-1': 196}, '平等机会': {'4': 527, '2': 930, '3': 347, '1': 415, '0': 457, '-1': 6}, '白手起家': {'2': 4350, '3': 1480, '1': 552, '4': 121, '0': 562, '-1': 31}, '成为富人': {'2': 887, '3': 273, '1': 112, '4': 189, '0': 132, '-1': 1}, '个体自由': {'4': 18807, '1': 1580, '2': 443, '3': 69, '-1': 8, '0': 83}, '安享晚年': {'3': 619, '2': 143, '4': 9, '1': 137, '0': 82, '-1': 13}, '收入足够': {'1': 55, '4': 54, '3': 80, '2': 142, '0': 70}, '个人努力': {'4': 224, '3': 1692, '2': 1174, '1': 195, '0': 29, '-1': 15}, '祖国强大': {'2': 180, '3': 132, '4': 76, '1': 8, '0': 34, '-1': 7}, '中国经济持续发展': {'3': 1, '2': 23, '4': 23, '1': 5, '0': 4}, '父辈更好': {'2': 10, '3': 8, '4': 3, '-1': 0}}, '201512': {'健康': {'2': 1147818, '4': 94955, '3': 481357, '0': 156841, '1': 111287, '-1': 36445}, '事业有成': {'3': 4830, '2': 7960, '1': 403, '4': 103, '0': 610, '-1': 95}, '发展机会': {'0': 741, '1': 1361, '2': 8713, '4': 3316, '3': 787, '-1': 22}, '生活幸福': {'3': 108968, '2': 273121, '4': 30661, '0': 4412, '1': 6311, '-1': 2389}, '有房': {'2': 28825, '0': 11180, '-1': 923, '3': 11035, '1': 3409, '4': 1029}, '出名': {'2': 28239, '0': 9427, '4': 1634, '3': 6812, '1': 5340, '-1': 1231}, '家庭幸福': {'3': 15566, '4': 2351, '1': 1930, '2': 40994, '-1': 531, '0': 1190}, '好工作': {'3': 9221, '2': 15060, '1': 1438, '4': 413, '0': 2389, '-1': 198}, '平等机会': {'0': 134, '2': 1378, '4': 642, '3': 475, '1': 169, '-1': 8}, '白手起家': {'2': 3470, '3': 1903, '0': 311, '1': 436, '-1': 25, '4': 38}, '成为富人': {'4': 171, '2': 917, '0': 317, '1': 54, '3': 243, '-1': 0}, '个体自由': {'4': 9237, '1': 1480, '2': 633, '3': 71, '0': 120, '-1': 7}, '安享晚年': {'3': 1454, '2': 374, '1': 146, '0': 264, '4': 11, '-1': 9}, '收入足够': {'2': 406, '1': 64, '4': 42, '3': 104, '0': 133}, '个人努力': {'3': 1367, '2': 1160, '4': 208, '1': 100, '0': 37, '-1': 6}, '祖国强大': {'3': 179, '2': 191, '4': 50, '0': 117, '1': 3, '-1': 11}, '中国经济持续发展': {'2': 30, '0': 7, '4': 37, '1': 3, '-1': 0, '3': 0}, '父辈更好': {'3': 9, '4': 66, '2': 8, '1': 1}}, '201601': {'健康': {'2': 1192247, '3': 503932, '1': 133970, '0': 140156, '4': 87496, '-1': 43044}, '事业有成': {'2': 9019, '3': 5588, '0': 516, '1': 387, '-1': 133, '4': 74}, '发展机会': {'2': 8465, '4': 6279, '3': 687, '1': 1145, '0': 911, '-1': 18}, '生活幸福': {'2': 277382, '3': 117100, '0': 4196, '4': 32292, '1': 9848, '-1': 2087}, '有房': {'2': 32438, '3': 10095, '0': 9459, '1': 3006, '-1': 981, '4': 636}, '出名': {'1': 6051, '3': 7566, '2': 29881, '0': 10071, '-1': 1236, '4': 1901}, '家庭幸福': {'2': 46955, '3': 14816, '1': 2049, '-1': 472, '4': 2113, '0': 1009}, '好工作': {'2': 15954, '3': 11386, '0': 2264, '1': 1354, '4': 537, '-1': 216}, '平等机会': {'2': 790, '4': 826, '1': 204, '3': 281, '0': 317, '-1': 15}, '白手起家': {'2': 3421, '0': 288, '-1': 21, '1': 376, '3': 1581, '4': 22}, '成为富人': {'2': 1047, '4': 141, '3': 400, '0': 395, '1': 80, '-1': 4}, '个体自由': {'4': 10743, '2': 473, '3': 69, '1': 1653, '0': 74, '-1': 13}, '安享晚年': {'3': 710, '2': 206, '0': 150, '1': 109, '4': 8, '-1': 6}, '收入足够': {'3': 100, '2': 177, '0': 74, '4': 86, '1': 298}, '个人努力': {'3': 1751, '2': 1650, '1': 120, '4': 207, '-1': 15, '0': 39}, '祖国强大': {'3': 194, '2': 496, '0': 97, '-1': 7, '4': 58, '1': 9}, '中国经济持续发展': {'4': 34, '2': 10, '1': 2, '3': 1, '0': 2}, '父辈更好': {'0': 4, '4': 55, '3': 8, '2': 7}}, '201602': {'健康': {'2': 1232272, '4': 74785, '3': 483766, '1': 107439, '0': 124600, '-1': 51339}, '事业有成': {'3': 5875, '2': 14129, '1': 714, '0': 365, '-1': 75, '4': 64}, '发展机会': {'2': 6803, '4': 3540, '3': 845, '1': 1008, '0': 618, '-1': 14}, '生活幸福': {'2': 260488, '3': 106513, '4': 29919, '-1': 2238, '1': 12720, '0': 3492}, '有房': {'3': 11017, '1': 3513, '2': 30598, '0': 9411, '-1': 1113, '4': 759}, '出名': {'2': 27659, '0': 8098, '-1': 829, '3': 7944, '1': 5653, '4': 1454}, '家庭幸福': {'3': 15982, '2': 49620, '0': 885, '4': 2548, '1': 2337, '-1': 729}, '好工作': {'1': 1912, '3': 10280, '2': 16634, '0': 2145, '4': 455, '-1': 258}, '平等机会': {'3': 224, '2': 739, '1': 157, '4': 635, '0': 262, '-1': 3}, '白手起家': {'2': 3234, '3': 1514, '1': 491, '0': 292, '4': 66, '-1': 23}, '成为富人': {'3': 544, '4': 268, '0': 363, '2': 738, '1': 77, '-1': 1}, '个体自由': {'4': 10273, '1': 1543, '2': 496, '3': 102, '0': 97, '-1': 5}, '安享晚年': {'3': 726, '2': 241, '0': 218, '-1': 47, '1': 282, '4': 10}, '收入足够': {'1': 624, '2': 385, '4': 35, '0': 60, '3': 180}, '个人努力': {'3': 1870, '2': 1140, '4': 193, '1': 141, '0': 33, '-1': 11}, '祖国强大': {'1': 5, '3': 58, '2': 179, '0': 23, '-1': 3, '4': 37}, '中国经济持续发展': {'4': 45, '0': 30, '1': 0, '2': 20}, '父辈更好': {'4': 49, '3': 12, '2': 15, '0': 0, '1': 3}}, '201603': {'健康': {'3': 282046, '2': 634175, '1': 67179, '0': 111063, '-1': 24781, '4': 62174}, '事业有成': {'3': 2628, '2': 4382, '4': 52, '0': 391, '1': 348, '-1': 33}, '发展机会': {'2': 4742, '4': 2358, '0': 828, '1': 1373, '3': 577, '-1': 63}, '生活幸福': {'2': 177475, '3': 68373, '4': 19133, '1': 9713, '-1': 1833, '0': 3264}, '有房': {'0': 8300, '2': 16019, '3': 7283, '-1': 679, '4': 1296, '1': 2769}, '出名': {'2': 17411, '3': 4573, '1': 3519, '0': 6100, '-1': 1088, '4': 1105}, '家庭幸福': {'2': 22142, '3': 10397, '0': 939, '4': 1862, '1': 1376, '-1': 276}, '好工作': {'3': 7029, '2': 11772, '1': 1524, '0': 1993, '-1': 217, '4': 437}, '平等机会': {'4': 355, '1': 228, '2': 936, '3': 289, '0': 230, '-1': 7}, '白手起家': {'2': 1980, '3': 1511, '1': 426, '0': 182, '-1': 14, '4': 28}, '成为富人': {'0': 243, '2': 577, '4': 116, '3': 138, '1': 25}, '个体自由': {'4': 5356, '3': 63, '2': 329, '1': 798, '0': 57, '-1': 10}, '安享晚年': {'3': 423, '2': 126, '0': 106, '1': 116, '-1': 12, '4': 7}, '收入足够': {'4': 70, '1': 107, '2': 860, '3': 118, '0': 60, '-1': 0}, '个人努力': {'3': 1356, '2': 880, '4': 161, '1': 117, '0': 133, '-1': 18}, '祖国强大': {'3': 58, '1': 8, '0': 37, '2': 130, '4': 22, '-1': 3}, '中国经济持续发展': {'4': 20, '1': 1, '2': 17, '0': 4}, '父辈更好': {'4': 20, '2': 6, '3': 4, '1': 0}}, '201604': {'健康': {'2': 725678, '1': 81375, '3': 303868, '0': 130101, '4': 72935, '-1': 22739}, '事业有成': {'1': 168, '2': 3369, '3': 2237, '-1': 34, '0': 303, '4': 26}, '发展机会': {'2': 5942, '4': 3962, '1': 964, '0': 900, '3': 997, '-1': 25}, '生活幸福': {'2': 161138, '3': 71229, '4': 17655, '-1': 1812, '1': 12628, '0': 3607}, '有房': {'2': 14319, '0': 7365, '1': 2469, '3': 7488, '4': 588, '-1': 452}, '出名': {'0': 7353, '2': 22025, '1': 4921, '3': 5364, '4': 1947, '-1': 1008}, '家庭幸福': {'2': 22970, '3': 9368, '0': 811, '4': 1942, '1': 1314, '-1': 255}, '好工作': {'0': 1910, '3': 8334, '2': 15114, '1': 1651, '4': 694, '-1': 218}, '平等机会': {'1': 168, '2': 627, '3': 218, '4': 371, '0': 133, '-1': 1}, '白手起家': {'2': 2879, '3': 1362, '1': 334, '0': 157, '4': 30, '-1': 15}, '成为富人': {'2': 586, '0': 265, '3': 162, '1': 32, '4': 146, '-1': 2}, '个体自由': {'4': 3968, '2': 381, '1': 1037, '0': 79, '-1': 9, '3': 72}, '安享晚年': {'3': 515, '2': 744, '1': 140, '-1': 19, '0': 90, '4': 4}, '收入足够': {'1': 38, '3': 92, '2': 187, '4': 60, '0': 97, '-1': 7}, '个人努力': {'3': 795, '2': 1676, '4': 216, '1': 95, '0': 33, '-1': 7}, '祖国强大': {'3': 61, '0': 60, '2': 245, '1': 13, '4': 17, '-1': 4}, '中国经济持续发展': {'4': 86, '0': 19, '2': 9, '1': 1}, '父辈更好': {'4': 6, '3': 8, '2': 8, '0': 2, '1': 0}}, '201605': {'健康': {'3': 381600, '2': 807215, '1': 98350, '0': 131169, '4': 84885, '-1': 28963}, '事业有成': {'3': 1702, '2': 4421, '1': 386, '0': 331, '-1': 37, '4': 51}, '发展机会': {'2': 6828, '3': 832, '0': 1174, '4': 2631, '1': 917, '-1': 25}, '生活幸福': {'2': 158384, '4': 15816, '1': 12460, '3': 67999, '0': 3626, '-1': 1659}, '有房': {'3': 9414, '0': 6122, '2': 13900, '1': 3177, '-1': 443, '4': 634}, '出名': {'1': 5696, '2': 24254, '0': 7921, '3': 6229, '-1': 1244, '4': 1728}, '家庭幸福': {'2': 25025, '3': 15078, '4': 2731, '1': 1088, '0': 1567, '-1': 328}, '好工作': {'1': 1379, '4': 409, '2': 12764, '3': 9811, '0': 2136, '-1': 250}, '平等机会': {'2': 793, '0': 340, '4': 470, '3': 311, '1': 192, '-1': 9}, '白手起家': {'3': 1654, '2': 2515, '-1': 17, '0': 188, '1': 292, '4': 51}, '成为富人': {'2': 611, '4': 124, '0': 128, '1': 28, '3': 141}, '个体自由': {'1': 1093, '4': 3527, '3': 76, '2': 531, '0': 93, '-1': 23}, '安享晚年': {'3': 703, '2': 868, '-1': 12, '0': 211, '1': 409, '4': 25}, '收入足够': {'2': 194, '4': 98, '0': 88, '3': 107, '1': 56, '-1': 0}, '个人努力': {'2': 31598, '3': 59014, '4': 2190, '1': 180, '0': 41, '-1': 12}, '祖国强大': {'2': 265, '0': 42, '4': 39, '3': 57, '-1': 1, '1': 4}, '中国经济持续发展': {'4': 19, '0': 4, '2': 12}, '父辈更好': {'3': 6, '4': 19, '0': 1, '2': 1, '1': 1}}, '201606': {'健康': {'2': 872267, '3': 405853, '1': 89692, '4': 78671, '0': 135058, '-1': 31578}, '事业有成': {'2': 3080, '0': 135, '3': 1499, '1': 229, '4': 22, '-1': 31}, '发展机会': {'3': 746, '4': 2790, '1': 818, '0': 1557, '2': 8120, '-1': 12}, '生活幸福': {'2': 131416, '4': 14523, '3': 54628, '1': 7161, '-1': 1526, '0': 3573}, '有房': {'3': 8599, '2': 13984, '1': 2676, '0': 7354, '-1': 466, '4': 684}, '出名': {'0': 9360, '2': 31549, '1': 7225, '3': 6382, '-1': 1691, '4': 1874}, '家庭幸福': {'2': 21607, '3': 9044, '4': 1954, '0': 998, '1': 961, '-1': 202}, '好工作': {'2': 10216, '3': 8056, '0': 2294, '1': 1652, '-1': 280, '4': 394}, '平等机会': {'3': 323, '2': 2131, '4': 403, '0': 128, '1': 189, '-1': 2}, '白手起家': {'2': 2488, '1': 312, '3': 1617, '0': 306, '4': 33, '-1': 19}, '成为富人': {'2': 512, '3': 157, '1': 31, '4': 101, '0': 110, '-1': 3}, '个体自由': {'4': 3190, '2': 689, '1': 1030, '3': 174, '-1': 23, '0': 89}, '安享晚年': {'3': 999, '2': 778, '0': 213, '1': 213, '4': 23, '-1': 6}, '收入足够': {'4': 79, '1': 93, '2': 231, '3': 78, '0': 74}, '个人努力': {'2': 997, '3': 917, '4': 171, '1': 122, '-1': 17, '0': 72}, '祖国强大': {'4': 46, '0': 79, '2': 252, '3': 72, '-1': 19, '1': 7}, '中国经济持续发展': {'4': 28, '2': 19, '3': 1, '1': 0, '0': 1}, '父辈更好': {'4': 6, '3': 10, '2': 16}}, '201607': {'健康': {'3': 300379, '2': 762181, '0': 125049, '1': 91974, '-1': 27040, '4': 79764}, '事业有成': {'2': 5280, '3': 2102, '0': 601, '-1': 27, '1': 405, '4': 42}, '发展机会': {'2': 6966, '0': 1799, '1': 736, '3': 575, '4': 3108, '-1': 34}, '生活幸福': {'2': 145795, '3': 60882, '4': 20154, '0': 5822, '1': 9457, '-1': 1816}, '有房': {'2': 14489, '3': 7686, '0': 7217, '1': 3055, '4': 723, '-1': 830}, '出名': {'3': 5890, '0': 9058, '1': 6657, '2': 32817, '-1': 973, '4': 1756}, '家庭幸福': {'2': 22960, '3': 9584, '4': 2066, '-1': 250, '1': 1162, '0': 1206}, '好工作': {'2': 10605, '3': 7756, '0': 2431, '1': 2230, '-1': 164, '4': 442}, '平等机会': {'4': 327, '3': 337, '0': 446, '2': 1684, '1': 323, '-1': 10}, '白手起家': {'3': 1966, '2': 2867, '1': 412, '0': 319, '-1': 9, '4': 49}, '成为富人': {'4': 132, '2': 699, '0': 247, '3': 252, '1': 59, '-1': 1}, '个体自由': {'2': 770, '4': 3290, '1': 709, '0': 111, '3': 71, '-1': 6}, '安享晚年': {'1': 169, '2': 615, '3': 1120, '0': 90, '4': 6, '-1': 7}, '收入足够': {'2': 274, '3': 89, '1': 105, '4': 128, '0': 82, '-1': 0}, '个人努力': {'2': 1053, '3': 737, '1': 74, '4': 151, '-1': 34, '0': 77}, '祖国强大': {'3': 346, '2': 641, '4': 195, '-1': 25, '0': 432, '1': 31}, '中国经济持续发展': {'4': 21, '2': 19, '0': 3}, '父辈更好': {'3': 13, '2': 21, '4': 7, '1': 1}}, '201608': {'健康': {'3': 171975, '2': 425797, '1': 51087, '0': 91409, '4': 41147, '-1': 12716}, '事业有成': {'3': 1012, '2': 1832, '0': 68, '1': 181, '4': 22, '-1': 21}, '发展机会': {'2': 4111, '0': 1103, '3': 312, '1': 704, '4': 1339, '-1': 10}, '生活幸福': {'2': 75897, '3': 27905, '0': 2461, '-1': 806, '4': 7735, '1': 3743}, '有房': {'3': 5245, '2': 9328, '1': 2254, '0': 6986, '-1': 379, '4': 589}, '出名': {'2': 20182, '0': 5777, '3': 4339, '1': 4629, '-1': 777, '4': 1290}, '家庭幸福': {'3': 5331, '2': 14293, '0': 942, '4': 1373, '-1': 182, '1': 603}, '好工作': {'2': 4947, '1': 763, '3': 4051, '0': 1245, '4': 160, '-1': 83}, '平等机会': {'2': 851, '4': 157, '3': 125, '1': 163, '0': 120}, '白手起家': {'2': 1187, '3': 825, '0': 284, '1': 318, '4': 125, '-1': 21}, '成为富人': {'0': 122, '1': 35, '2': 425, '3': 90, '4': 69}, '个体自由': {'4': 1846, '1': 238, '2': 956, '3': 45, '0': 64, '-1': 4}, '安享晚年': {'2': 496, '3': 483, '1': 90, '0': 53, '4': 15, '-1': 2}, '收入足够': {'2': 172, '4': 55, '3': 78, '1': 164, '0': 224}, '个人努力': {'3': 428, '2': 405, '-1': 23, '4': 37, '1': 76, '0': 59}, '祖国强大': {'2': 434, '3': 164, '-1': 14, '4': 51, '0': 96, '1': 12}, '中国经济持续发展': {'4': 30, '2': 17, '0': 5, '1': 0}, '父辈更好': {'3': 4, '-1': 1, '2': 4, '4': 3, '1': 0, '0': 0}}, '201609': {'健康': {'2': 585354, '3': 228287, '1': 61960, '0': 90467, '-1': 11715, '4': 59081}, '事业有成': {'2': 2192, '3': 938, '1': 161, '-1': 23, '0': 47, '4': 26}, '发展机会': {'4': 1749, '1': 675, '2': 5629, '0': 980, '3': 492, '-1': 11}, '生活幸福': {'2': 84388, '3': 37580, '4': 9843, '1': 6349, '0': 2126, '-1': 727}, '有房': {'0': 8055, '2': 12960, '1': 3171, '3': 6012, '4': 1189, '-1': 468}, '出名': {'1': 4867, '3': 5357, '0': 4958, '2': 18343, '4': 1684, '-1': 744}, '家庭幸福': {'2': 22245, '3': 8727, '0': 585, '4': 1500, '1': 890, '-1': 239}, '好工作': {'2': 6465, '3': 5330, '0': 1213, '1': 726, '4': 226, '-1': 68}, '平等机会': {'4': 210, '3': 107, '0': 86, '2': 462, '1': 130, '-1': 2}, '白手起家': {'3': 779, '2': 1829, '1': 232, '0': 294, '4': 43, '-1': 14}, '成为富人': {'2': 608, '-1': 3, '1': 16, '4': 75, '3': 156, '0': 113}, '个体自由': {'4': 2841, '2': 455, '1': 211, '0': 39, '3': 44, '-1': 3}, '安享晚年': {'2': 693, '3': 550, '1': 91, '0': 85, '4': 42, '-1': 24}, '收入足够': {'2': 128, '0': 93, '1': 27, '4': 37, '3': 57}, '个人努力': {'2': 349, '3': 427, '1': 51, '0': 31, '4': 148, '-1': 3}, '祖国强大': {'2': 395, '3': 143, '0': 56, '4': 70, '-1': 13, '1': 2}, '中国经济持续发展': {'4': 92, '2': 138, '1': 231, '0': 104}, '父辈更好': {'4': 2, '2': 9, '3': 1}}, '201610': {'健康': {'2': 828809, '3': 281195, '-1': 14153, '0': 120300, '1': 86859, '4': 102963}, '事业有成': {'3': 978, '2': 2545, '1': 241, '4': 28, '0': 167, '-1': 22}, '发展机会': {'0': 1230, '2': 5480, '4': 2455, '1': 574, '3': 464, '-1': 8}, '生活幸福': {'2': 126213, '3': 42622, '1': 5274, '4': 14812, '0': 2508, '-1': 952}, '有房': {'1': 3098, '2': 13992, '3': 5882, '0': 7891, '4': 970, '-1': 602}, '出名': {'2': 31042, '0': 5533, '1': 5988, '3': 5456, '-1': 687, '4': 2064}, '家庭幸福': {'2': 32070, '3': 8109, '1': 725, '4': 2108, '0': 825, '-1': 266}, '好工作': {'2': 8747, '3': 7368, '0': 1456, '1': 870, '-1': 148, '4': 195}, '平等机会': {'4': 210, '2': 520, '0': 319, '3': 157, '1': 240, '-1': 1}, '白手起家': {'2': 3514, '3': 795, '1': 362, '0': 271, '4': 38, '-1': 7}, '成为富人': {'2': 582, '0': 200, '3': 135, '4': 56, '1': 11}, '个体自由': {'0': 42, '4': 3414, '1': 687, '2': 536, '3': 51, '-1': 4}, '安享晚年': {'2': 2437, '0': 136, '3': 558, '1': 144, '-1': 10, '4': 19}, '收入足够': {'0': 69, '2': 555, '3': 73, '4': 70, '-1': 1, '1': 29}, '个人努力': {'2': 679, '3': 439, '1': 479, '4': 68, '0': 70, '-1': 10}, '祖国强大': {'0': 96, '2': 587, '4': 91, '3': 236, '1': 159, '-1': 14}, '中国经济持续发展': {'4': 29, '0': 78, '2': 16, '1': 5, '3': 21}, '父辈更好': {'2': 9, '0': 1, '3': 6, '4': 0}}, '201611': {'健康': {'2': 800708, '4': 119385, '3': 265380, '1': 71962, '0': 93818, '-1': 20177}, '事业有成': {'3': 1089, '2': 2162, '1': 155, '0': 87, '4': 38, '-1': 35}, '发展机会': {'2': 3861, '0': 1263, '3': 370, '4': 2022, '1': 514, '-1': 16}, '生活幸福': {'2': 105559, '3': 39120, '4': 11253, '-1': 831, '1': 4004, '0': 1985}, '有房': {'3': 4767, '2': 9557, '1': 2082, '0': 4507, '-1': 393, '4': 599}, '出名': {'1': 4534, '2': 19593, '4': 1463, '0': 4281, '3': 4341, '-1': 570}, '家庭幸福': {'2': 28242, '-1': 275, '4': 2271, '3': 5744, '1': 959, '0': 551}, '好工作': {'0': 1174, '3': 5984, '2': 6461, '1': 807, '4': 247, '-1': 136}, '平等机会': {'0': 195, '2': 509, '4': 237, '3': 182, '1': 393, '-1': 5}, '白手起家': {'2': 1461, '1': 371, '3': 1198, '0': 825, '4': 22, '-1': 15}, '成为富人': {'0': 183, '2': 477, '3': 93, '4': 51, '1': 37, '-1': 0}, '个体自由': {'4': 2561, '2': 702, '1': 830, '3': 42, '0': 62, '-1': 7}, '安享晚年': {'2': 866, '0': 72, '3': 866, '1': 233, '4': 10, '-1': 16}, '收入足够': {'3': 155, '1': 57, '2': 128, '4': 41, '0': 53}, '个人努力': {'1': 287, '0': 26, '3': 450, '2': 952, '4': 61, '-1': 15}, '祖国强大': {'2': 312, '4': 56, '-1': 17, '0': 152, '3': 267, '1': 16}, '中国经济持续发展': {'4': 19, '2': 5, '0': 6, '3': 0}, '父辈更好': {'2': 4, '4': 1, '3': 3, '0': 0}}, '201612': {'健康': {'2': 524712, '3': 170156, '1': 53938, '4': 45978, '0': 81625, '-1': 12138}, '事业有成': {'3': 838, '2': 1513, '1': 117, '0': 56, '4': 19, '-1': 23}, '发展机会': {'4': 1405, '2': 3898, '3': 258, '0': 772, '1': 342, '-1': 8}, '生活幸福': {'2': 78175, '3': 28502, '4': 7433, '1': 3363, '-1': 616, '0': 1732}, '有房': {'3': 3839, '0': 5237, '2': 8761, '4': 603, '1': 2034, '-1': 333}, '出名': {'1': 3733, '-1': 501, '2': 16192, '3': 3443, '0': 3966, '4': 1408}, '家庭幸福': {'2': 17900, '3': 4859, '4': 1659, '0': 465, '1': 568, '-1': 424}, '好工作': {'2': 9950, '3': 6960, '-1': 118, '1': 830, '4': 180, '0': 1287}, '平等机会': {'3': 124, '2': 1027, '4': 157, '1': 87, '0': 56, '-1': 1}, '白手起家': {'3': 1027, '2': 1744, '1': 214, '-1': 13, '0': 122, '4': 25}, '成为富人': {'1': 25, '0': 80, '3': 68, '4': 50, '2': 258, '-1': 2}, '个体自由': {'4': 2137, '2': 377, '1': 492, '3': 29, '0': 28, '-1': 3}, '安享晚年': {'2': 665, '3': 498, '1': 79, '0': 58, '4': 4, '-1': 10}, '收入足够': {'3': 76, '4': 32, '1': 25, '2': 75, '0': 65, '-1': 0}, '个人努力': {'2': 341, '3': 260, '0': 21, '1': 63, '4': 48, '-1': 4}, '祖国强大': {'-1': 20, '0': 76, '3': 213, '2': 226, '4': 105, '1': 9}, '中国经济持续发展': {'1': 0, '4': 11, '0': 5, '2': 3, '3': 0}, '父辈更好': {'2': 2, '3': 2, '4': 0, '1': 0}}}
    result_dic = dismiss_unknowemotion(result_dic)
    result_dic = trans_result2Percent(result_dic)
    time_list = get_timeList(result_dic)
    result_data = echarts_output(result_dic,emotion_list)
    keyword_stdouput()

    print('option settings')
    option_stdoutput(time_list)
    print(emotion_list)