#!/usr/bin/env python

# _*_ coding:utf-8 _*_

'''

@author: diw

@contact: di.W@hotmail.com

@file: topic_location

@time: 2018/9/29 2:37

@desc:

'''

import topic_sta1
from topic_sta1 import topic
from topic_sta1 import keywords_list
from numba import jit

weibofilefolder = 'D:/chinadream/data'
north_city = ['北京','天津','内蒙古','新疆','河北','甘肃','宁夏','山西','陕西','青海','山东','河南','安徽','辽宁','吉林','黑龙江']
south_city = ['江苏','浙江','上海','湖北','湖南','四川','重庆','贵州','云南','广西','江西','福建','广东','海南','西藏','台湾','香港','澳门']

@jit
def list_add(a,b):
    c = []
    for i in range(len(a)):
        c.append(a[i]+b[i])
    return c
@jit
def add_data(output, input_list, keyword):
    if(keyword not in output.keys()):
        output[keyword] = input_list
    else:
        output[keyword] = list_add(output[keyword],input_list)
    return output

def get_echartsdata(output):
    region_list = []
    series_dic = {}
    for region in output.keys():
        region_list.append(region)
    for keyword_label in keywords_list:
        current_list = []
        index = keywords_list.index(keyword_label)
        for region in region_list:
            current_region_list = output[region]
            if (index <= len(current_region_list) - 1):
                current_list.append(current_region_list[index])
            else:
                current_list.append(0)
        series_dic[keyword_label] = current_list

    for series, series_list in series_dic.items():
        #累积直方图
        print(series)
        print(series_list)
        print('______________')
    # xAisx
    print(region_list)
    print(output)

@jit
def calc_sum(temp_list):
    sum = 0
    for temp in temp_list:
        sum += temp
    return sum


def region_calc(output_dic):
    output = {}
    for location_str, count_list in output_dic.items():
        location_list = location_str.split()
        # 抛弃未知地理位置的数据
        if(len(location_list) == 0):
            continue

        city = location_list[0]
        if(city == '其他'):
            output = add_data(output, count_list, '其他')
        elif(city == '海外'):
            output = add_data(output, count_list, '海外')
        elif (city in north_city):
            output = add_data(output, count_list, '北方')
        elif (city in south_city):
            output = add_data(output, count_list, '南方')
        else:
            print(city)

    percent_output = {}
    #pecent_list
    for region, current_list in output.items():
        sum = calc_sum(current_list)
        temp_list = []
        for i in range(len(current_list)):
            temp_list.append(float(current_list[i])/sum)
        percent_output[region] = temp_list
    return percent_output

def province_percent(calc_dic):
    output_dic = {}
    for location_detailed,current_list in calc_dic.items():
        province_list = location_detailed.split()
        if(len(province_list) == 0):
            continue
        province = province_list[0]
        output_dic[province] = []
        sum = calc_sum(current_list)
        temp_list = []
        for i in range(len(current_list)):
            temp_list.append(float(current_list[i])/sum)
        output_dic[province] = temp_list
    return output_dic


if __name__ == '__main__':
    file_path_list = topic_sta1.getAllFile(weibofilefolder)
    topic_sta1.keyword_location(file_path_list)
