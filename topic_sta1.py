# -*- coding: utf-8 -*-
# @Author: di.W
# @Date: 2018-09-23 19:22:25
# @Last Modified by:   di.W
# @Last Modified time: 2018-09-23 19:22:25
# @Description:  */

debug = 0
from numba import jit
from time import time
import jieba
import os
import json
import topic_cla
import filer
import pymongo
import pickle

# the uppest path of weibo data document
weibofilefolder = 'D:/chinadream/data'
north_city = ['北京','天津','内蒙古','新疆','河北','甘肃','宁夏','山西','陕西','青海','山东','河南','安徽','辽宁','吉林','黑龙江']
south_city = ['江苏','浙江','上海','湖北','湖南','四川','重庆','贵州','云南','广西','江西','福建','广东','海南','西藏','台湾','香港','澳门']
# return [filepath]
def getAllFile(folderpath):
    temp_list = []
    folderlist = os.listdir(folderpath)
    temp_list = [weibofilefolder + '/' + filename + '/' + filename for filename in folderlist]
    return temp_list



# 获得采集日期
def getFileTime(filepath):
    time = filepath.strip().split('/')[-1].split('.')[0]
    return time


# input line.split('\t')
# 存在 ,
def getKeywordList(line_section):
    return line_section[:-1]


# input line.split('\t')
def getText(line_section):
    if(type(line_section) == list):
        temp_dic_str = line_section[-1].strip()
        temp_dic = json.loads(temp_dic_str)
        return temp_dic['text']
    elif(type(line_section) == dict):
        return(line_section['text'])
    else:
        print('type error')

def getLocation(line_section):
    if(type(line_section) == list):
        temp_dic_str = line_section[-1].strip()
        temp_dic = json.loads(temp_dic_str)
        return temp_dic['user']['location']
    elif(type(line_section) == dict):
        return(line_section['user']['location'])
    else:
        print('type error')

def getFollowers(line_section):
    if(type(line_section) == list):
        temp_dic_str = line_section[-1].strip()
        temp_dic = json.loads(temp_dic_str)
        return temp_dic['user']['followers_count']
    elif(type(line_section) == dict):
        return(line_section['user']['followers_count'])
    else:
        print('key value: \'followers_count\' not found ')

def getFriends(line_section):
    if(type(line_section) == list):
        temp_dic_str = line_section[-1].strip()
        temp_dic = json.loads(temp_dic_str)
        return temp_dic['user']['friends_count']
    elif(type(line_section) == dict):
        return(line_section['user']['friends_count'])
    else:
        print('key value: \'friends_count\' not found ')

# predict topic; len(jieba.cut)<5 return -1
topic = ['社会', '国际', '体育', '科技', '娱乐', '财经', '军事']


def getTopic(weibo):
    return topic_cla.predict(weibo)

#keyword切分
def conntoMongoWeibo():
    conn = pymongo.MongoClient('127.0.0.1',
                   27017,
                   username='wd',
                   password='wd123456',
                  )
    db = conn.weiboDB
    return db

#keyword不切分
def conntoMongoWeiboNSeg():
    conn = pymongo.MongoClient('127.0.0.1',
                   27017,
                   username='wd',
                   password='wd123456',
                  )
    db = conn.weiboDBNSeg
    return db

@jit
def word_coOcurrence(input_dic, word_list):
    for keyword1 in word_list:
        keyword1 = keyword1.replace(',', '')
        for keyword2 in word_list:
            keyword2 = keyword2.replace(',', '')
            if (keyword1 == keyword2):
                continue
            input_dic[keyword1][keywords_list.index(keyword2)] += 1
    return input_dic

# return dic[keyword] = (topic_count)['社会', '国际', '体育', '科技', '娱乐', '财经', '军事']
def topic_keyword(file_paht_list):
    dismiss_count = 0
    output_dic = {}

    for current_file in file_paht_list:
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')
                keyword_list = getKeywordList(line_section)
                # print(keyword_list)
                current_text = getText(line_section)

                # dismiss weibo which is too short(<5)
                current_text = filer.filer(current_text)
                word_list = [word for word in jieba.cut(current_text)]
                if (len(word_list) < 5):
                    dismiss_count += 1

                    continue

                current_topic = getTopic(current_text)
                for keyword in keyword_list:
                    keyword = keyword.replace(',','')
                    if (keyword not in output_dic.keys()):
                        print(keyword)
                        output_dic[keyword] = [0 for i in range(len(topic))]
                    output_dic[keyword][topic.index(current_topic)] += 1
            e_t = time()
            print('current file process time: ' + str(e_t - s_t))
        print(output_dic)
        print('dismiss count: ' + str(dismiss_count))

# return dic[str(follower)] = (topic_count)['社会', '国际', '体育', '科技', '娱乐', '财经', '军事']
def topic_followers(file_paht_list):
    dismiss_count = 0

    output_dic = {}

    for current_file in file_paht_list:
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')
                followers = getFollowers(line_section)
                current_text = getText(line_section)
                current_text = filer.filer(current_text)
                word_list = [word for word in jieba.cut(current_text)]
                if (len(word_list) < 5):
                    dismiss_count += 1
                    continue
                current_topic = getTopic(current_text)
                if (str(followers) not in output_dic.keys()):
                    print(followers)
                    output_dic[str(followers)] = [0 for i in range(len(topic))]
                output_dic[str(followers)][topic.index(current_topic)] += 1
            e_t = time()


        print(output_dic)
        print('dismiss count: ' + str(dismiss_count))
        print('current collection process time: ' + str(e_t - s_t))

    # 存储
    output_file = open('data/topic_follower.pickle', 'wb')
    pickle.dump(output_dic, output_file)
    output_file.close()

    # # 读取
    # output_file = open('data/topic_follower.pickle', 'rb')
    # output_dic = pickle.load(output_file)
    # print(output_dic)
    # print(output_dic['1555984'])


# return dic[str(friend)] = (topic_count)['社会', '国际', '体育', '科技', '娱乐', '财经', '军事']
def topic_friends(file_paht_list):
    dismiss_count = 0

    output_dic = {}


    for current_file in file_paht_list:
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')
                friends = getFriends(line_section)
                current_text = getText(line_section)
                current_text = filer.filer(current_text)
                word_list = [word for word in jieba.cut(current_text)]
                if (len(word_list) < 5):
                    dismiss_count += 1
                    continue
                current_topic = getTopic(current_text)
                if (str(friends) not in output_dic.keys()):
                    print(friends)
                    output_dic[str(friends)] = [0 for i in range(len(topic))]
                output_dic[str(friends)][topic.index(current_topic)] += 1
        e_t = time()
        print(output_dic)
        print('dismiss count: ' + str(dismiss_count))
        print('current collection process time: ' + str(e_t - s_t))
    # 存储
    output_file = open('data/topic_friends.pickle', 'wb')
    pickle.dump(output_dic, output_file)
    output_file.close()

    # # 读取
    # output_file = open('data/topic_friends.pickle', 'rb')
    # output_dic = pickle.load(output_file)
    # print(output_dic)
    # print(output_dic['1555984'])

# return dic[location] = (topic_count)['社会', '国际', '体育', '科技', '娱乐', '财经', '军事']
def topic_location(file_paht_list):
    dismiss_count = 0

    output_dic = {}

    for current_file in file_paht_list:
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')

                location = getLocation(line_section)
                current_text = getText(line_section)
                current_text = filer.filer(current_text)
                word_list = [word for word in jieba.cut(current_text)]
                if (len(word_list) < 5):
                    dismiss_count += 1
                    continue
                current_topic = getTopic(current_text)
                if (location not in output_dic.keys()):
                    print(location)
                    output_dic[location] = [0 for i in range(len(topic))]
                output_dic[location][topic.index(current_topic)] += 1
            e_t = time()
        print(output_dic)
        print('dismiss count: ' + str(dismiss_count))
        print('current collection process time: ' + str(e_t - s_t))

# return output_list = ['社会', '国际', '体育', '科技', '娱乐', '财经', '军事']
def topic_percent(file_paht_list):
    dismiss_count = 0
    output_list = [0 for i in range(len(topic))]
    for current_file in file_paht_list:
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')

                current_text = getText(line_section)

                # dismiss weibo which is too short(<5)
                current_text = filer.filer(current_text)
                word_list = [word for word in jieba.cut(current_text)]
                if (len(word_list) < 5):
                    dismiss_count += 1
                    continue
                current_topic = getTopic(current_text)
                output_list[topic.index(current_topic)] += 1
            e_t = time()
            print(output_list)
            print('dismiss count: ' + str(dismiss_count))
            print('current collection process time: ' + str(e_t - s_t))


def keyword_percent(file_paht_list):
    dismiss_count = 0
    output_dic_gt5 = {}
    output_dic_all = {}

    for current_file in file_paht_list:
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')

                current_text = getText(line_section)
                keyword_list = getKeywordList(line_section)
                # dismiss weibo which is too short(<5)
                current_text = filer.filer(current_text)
                word_list = [word for word in jieba.cut(current_text)]

                # 统计所有
                for keyword in keyword_list:
                    keyword = keyword.replace(',', '')
                    if (keyword not in output_dic_all.keys()):
                        print(keyword)
                        output_dic_all[keyword] = 0
                    output_dic_all[keyword] += 1

                if (len(word_list) < 5):
                    dismiss_count += 1
                    continue

                for keyword in keyword_list:
                    keyword = keyword.replace(',', '')
                    if (keyword not in output_dic_gt5.keys()):
                        print(keyword)
                        output_dic_gt5[keyword] = 0
                    output_dic_gt5[keyword] += 1
            e_t = time()
            print('all')
            print(output_dic_all)
            print('greater than 5')
            print(output_dic_gt5)
            print('dismiss count: ' + str(dismiss_count))
            print('current collection process time: ' + str(e_t - s_t))

# return dic[location] = (keyword_count)['健康','事业有成','发展机会','生活幸福','有房','出名','家庭幸福','好工作','平等机会','白手起家','成为富人','个体自由','安享晚年','收入足够','个人努力','祖国强大','中国经济持续发展','父辈更好']
keywords_list = ['健康','事业有成','发展机会','生活幸福','有房','出名','家庭幸福','好工作','平等机会','白手起家','成为富人','个体自由','安享晚年','收入足够','个人努力','祖国强大','中国经济持续发展','父辈更好']
def keyword_location(file_paht_list):
    dismiss_count = 0

    output_dic = {}

    for current_file in file_paht_list:
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')
                location = getLocation(line_section)
                keyword_list = getKeywordList(line_section)
                current_text = getText(line_section)
                current_text = filer.filer(current_text)
                word_list = [word for word in jieba.cut(current_text)]
                if (len(word_list) < 5):
                    dismiss_count += 1
                    continue

                if (location not in output_dic.keys()):
                    print(location)
                    output_dic[location] = [0 for i in range(len(keywords_list))]
                for keyword in keyword_list:
                    keyword = keyword.replace(',', '')
                output_dic[location][keywords_list.index(keyword)] += 1
            e_t = time()
        print(output_dic)
        print('dismiss count: ' + str(dismiss_count))
        print('current collection process time: ' + str(e_t - s_t))

def keyword_coOccurrence(file_path_list):
    dismiss_count = 0

    output_dic = {}
    for keyword in keywords_list:
        output_dic[keyword] = [0 for i in range(len(keywords_list))]

    for current_file in file_path_list:
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')
                current_keyword_list = getKeywordList(line_section)


                if(len(current_keyword_list) <= 1):
                    continue
                output_dic = word_coOcurrence(output_dic, current_keyword_list)
            e_t = time()
        print(output_dic)
        print('dismiss count: ' + str(dismiss_count))
        print('current collection' + str(current_file) + 'process time: ' + str(e_t - s_t))


if __name__ == '__main__':
    # topic_keyword
    allfile = getAllFile(weibofilefolder)
    # print(allfile)
    # topic_keyword(allfile)
    count = 0

    s_t = time()
    db = conntoMongoWeiboNSeg()
    collectionlist = db.collection_names()
    for collection in collectionlist:
        result_iter = db[collection].find()
        for result in result_iter:
            count += 1
    #     e_t = time()
    #     print('current collection process time: ' + str(e_t - s_t))

    # s_t = time()
    # for current_file in allfile:
    #     with open(current_file, 'r', encoding='utf-8') as f:
    #         for line in f:
    #             count+=1
    e_t = time()
    print('current collection process time: ' + str(e_t - s_t))

