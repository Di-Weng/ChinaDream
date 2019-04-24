# _*_ coding:utf-8 _*_

'''

@author: diw

@contact: di.W@hotmail.com

@file: keyword_city

@time: 2018/10/23 16:39

@desc:

'''
from multiprocessing import Pool
import threading
import topic_sta1
import time
import os
import fcntl
import multiprocessing
from topic_sta1 import getText,getKeywordList,getLocation,getMood
weibofilefolder = '/Volumes/data/chinadream/data'

def collect_time_emotion_city_file(current_file):
    ignore_region = ['其他','海外']
    output_file_1 = '/Volumes/data/chinadream/keyword_emotion_location/'
    output_file_2 = '/Volumes/data/chinadream/time_keyword_emotion_location/'

    print(current_file)
    with open(current_file, 'r', encoding='utf-8') as f:
        line_count = 0
        for line in f:
            line_section = line.split('\t')
            current_text = getText(line_section)
            current_keyword_list = getKeywordList(line_section)
            current_detailed_location = getLocation(line_section)
            current_location_list = current_detailed_location.split()
            current_mood = getMood(line_section)
            if(len(str(current_mood)) == 0):
                continue

            if(len(str(current_location_list)) == 0):
                continue
            province = current_location_list[0]

            if(province in ignore_region):
                continue
            elif(province == '香港' or province == '澳门'):
                city = province
            else:
                if(len(current_location_list) < 2):
                    continue
                city = current_location_list[1]
            line_count += 1
            time_stamp = current_file.split('/')[-1].split('.')[0]
            log_file = open('/Volumes/data/chinadream/log/' + time_stamp + '.txt', 'w+',encoding='utf-8')
            log_file.write(str(line_count))
            for current_keyword in current_keyword_list:
                temp1 = current_file.split('/')[-1]
                temp2 = temp1.split('.')[0]
                current_out_path_1 = output_file_1 + str(current_mood) + '/' + current_keyword
                current_out_path_2_time = output_file_2 + temp2 + '/' + str(current_mood)
                # print(current_out_path_1)
                # if(not os.path.exists(current_out_path_1)):
                #     os.makedirs(current_out_path_1)
                if (not os.path.exists(current_out_path_2_time)):
                    os.makedirs(current_out_path_2_time)


                with open(current_out_path_1 + '/' + city + '.txt', 'a+', encoding='utf-8') as keyword_location_file:
                    fcntl.flock(keyword_location_file.fileno(), fcntl.LOCK_EX)  # 加锁
                    keyword_location_file.write(current_text)
                    keyword_location_file.write('\n')

                current_out_path_2_time_keyword = current_out_path_2_time + '/' + current_keyword

                if (not os.path.exists(current_out_path_2_time_keyword)):
                    os.mkdir(current_out_path_2_time_keyword)

                #各个线程操作不同的文件，不需要加锁
                time_keyword_location_file = open(current_out_path_2_time_keyword + '/' + city + '.txt', 'a+',
                                                  encoding='utf-8')
                time_keyword_location_file.write(current_text)
                time_keyword_location_file.write('\n')
                time_keyword_location_file.close()

        e_t = time()
    log_file.close()
    print('current_file:' + current_file)
    print('current file process time: ' + str(e_t - s_t))
    return 1

def store_data():
    file_path_list = topic_sta1.getAllFile(weibofilefolder)
    topic_sta1.collect_city_file(file_path_list)

def store_data_2():
    topic_sta1.collect_emotion_city_file(file_path_list)

def make_dirs():
    output_file_1 = '/Volumes/data/chinadream/keyword_emotion_location/'
    keywords_folder_list = ['健康','事业有成','发展,机会','生活,幸福','有房','出名','家庭,幸福',
                            '好工作','平等,机会','白手起家','成为,富人','个体,自由','安享晚年','收入,足够','个人努力',
                            '祖国强大','中国经济,持续发展','父辈,更好']
    emotion = [-1,0,1,2,3,4]
    for current_emotion in emotion:
        for current_keyword in keywords_folder_list:
            current_folder = output_file_1 + str(current_emotion) + '/' + current_keyword
            if (not os.path.exists(current_folder)):
                os.makedirs(current_folder)



if __name__ == '__main__':

    # 不带情感
    # store_data()

    # 带时间_情感
    # make_dirs()
    #
    file_path_list = topic_sta1.getAllFile(weibofilefolder)
    # for i in file_path_list:
    #     t = threading.Thread(target=collect_time_emotion_city_file, args=(i,))
    #     t.start()

    pool = multiprocessing.Pool(processes=8)
    for i in file_path_list:
        pool.apply_async(topic_sta1.multi_collect_time_emotion_city_file_nospam,(i,))
    pool.close()
    pool.join()
    #统计各keyword 和城市的微博语料数
    # topic_sta1.calc_city_doc()