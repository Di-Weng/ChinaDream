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
import jieba
from gensim import corpora
from gensim.models import LdaModel, TfidfModel
from gensim.test.utils import datapath
from gensim.models import LdaMulticore
import codecs
from collections import defaultdict
import gc
from random import randint
import linecache

# the uppest path of weibo data document
weibofilefolder = '/Volumes/chinadream/data'
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

def getMood(line_section):
    if(type(line_section) == list):
        temp_dic_str = line_section[-1].strip()
        temp_dic = json.loads(temp_dic_str)
        return temp_dic['mood']
    elif(type(line_section) == dict):
        return(line_section['mood'])
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
def conntoMongoWeibo(ServerURL = '127.0.0.1'):
    conn = pymongo.MongoClient(ServerURL,
                   27017,
                   username='wd',
                   password='wd123456',
                  )
    db = conn.weiboDB
    return db

#keyword不切分
def conntoMongoWeiboNSeg(ServerURL = '127.0.0.1'):
    conn = pymongo.MongoClient(ServerURL,
                   27017,
                   username='wd',
                   password='wd123456',
                  )
    db = conn.weiboDBNSeg
    return db

#按无时间维度 先按keyword划分collection，每个collection为该keyword下所有城市的话题分布
def conntoMongoKeywordLocation(ServerURL = '127.0.0.1'):
    conn = pymongo.MongoClient(ServerURL,
                   27017,
                   username='wd',
                   password='wd123456',
                  )
    # db = conn.weiboProvince_text
    db = conn.keywordLocation
    return db

#按无时间维度 keywordLocation 的话题
def conntoMongoKeywordLocation_topic(ServerURL = '127.0.0.1'):
    conn = pymongo.MongoClient(ServerURL,
                   27017,
                   username='wd',
                   password='wd123456',
                  )
    # db = conn.weiboProvince_text
    db = conn.keywordLocationTopic
    return db

#keyword统计城市微博数量
def conntoMongokeywordLocation_sta(ServerURL = '127.0.0.1'):
    conn = pymongo.MongoClient(ServerURL,
                   27017,
                   username='wd',
                   password='wd123456',
                  )
    db = conn.keywordLocation_sta
    return db


@jit
def word_coOcurrence(input_dic, word_list):
    for keyword1 in word_list:
        keyword1 = keyword1.replace(',', '')
        input_dic['seperate'][keyword1] += 1
        for keyword2 in word_list:
            keyword2 = keyword2.replace(',', '')
            if (keyword1 == keyword2):
                continue
            input_dic['together'][keyword1][keywords_list.index(keyword2)] += 1
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

#边权重：jaccard系数： 共同出现/（各自单独出现之和-共同出现）
def keyword_coOccurrence(file_path_list):
    dismiss_count = 0

    output_dic = {}
    output_dic['together'] = {}
    output_dic['seperate'] = {}
    for keyword in keywords_list:
        output_dic['together'][keyword] = [0 for i in range(len(keywords_list))]
        output_dic['seperate'][keyword] = 0

    for current_file in file_path_list:
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')
                current_keyword_list = getKeywordList(line_section)


                if(len(current_keyword_list) == 0):
                    continue
                output_dic = word_coOcurrence(output_dic, current_keyword_list)
            e_t = time()
        print(output_dic)
        print('dismiss count: ' + str(dismiss_count))
        print('current collection' + str(current_file) + 'process time: ' + str(e_t - s_t))

# memory error
def keyword_location_lda(mongo_server = '127.0.0.1'):
    jieba.load_userdict("data/user_dict.txt")
    stop_word = []
    weibocityfilefolder = '/Volumes/chinadream/city/'
    keyword_finished = []
    db = conntoMongoKeywordLocation_topic()
    for keyword_result in db['topic'].find():
        keyword_finished.append(keyword_result['keyword'])

    with open('data/stop_word.txt', 'r', encoding='utf-8') as sw_f:
        for item in sw_f:
            stop_word.append(item.strip())

    keyword_folder = '/Volumes/chinadream/keyword_location/'
    folderlist = os.listdir(keyword_folder)
    for current_keyword in folderlist:
        if(current_keyword in keyword_finished):
            continue
        print(current_keyword)
        current_keyword_cut_list = current_keyword.split(',')
        current_keyword_banned_list = []

        # 全切
        for temp1 in current_keyword_cut_list:
            cut_list = jieba.cut(temp1)
            for temp2 in cut_list:
                current_keyword_banned_list.append(temp2)

        current_keyword_folder = keyword_folder + current_keyword + '/'
        current_city_file_list = os.listdir(current_keyword_folder)

        #corpus_text 里的每个list代表一个城市的所有文本
        corpus_text = []
        corpus_city = {}
        count = 0
        for current_city_file in current_city_file_list:
            print(current_city_file)
            corpus_numbers = 0
            origin_text = []
            open_keyword_file_path = current_keyword_folder + current_city_file
            open_keyword_file = linecache.getlines(open_keyword_file_path)
            # open_keyword_file = open(open_keyword_file_path,'r',encoding='utf-8')
            temp_line_num = len(open_keyword_file)
            max_weiboDoc = 5000
            if(temp_line_num < max_weiboDoc):
                for temp_line_lineNum in range(temp_line_num):
                    temp_line = open_keyword_file[temp_line_lineNum]
                    current_topic = getTopic(temp_line)
                    if(current_topic == '娱乐'):
                        continue

                    weibo_origin = filer.filer(temp_line).replace('/','')
                    if (len(weibo_origin) == 0):
                        continue
                    weibo_cut = list(jieba.cut(weibo_origin))
                    weibo_cut_list = []
                    for items in weibo_cut:
                        if (items not in stop_word and len(items.strip()) > 0):
                            if(items in current_keyword_banned_list):
                                continue
                            weibo_cut_list.append(items)
                    if(len(weibo_cut_list) < 5):
                        continue
                    for current_cut in weibo_cut_list:
                        origin_text.append(current_cut)
            else:
                used_set = set()
                linenumber_list = [i for i in range(temp_line_num)]

                while(len(used_set) < max_weiboDoc or len(linenumber_list) > 0):
                    if(len(linenumber_list) == 0):
                        break
                    elif(len(linenumber_list) == 1):
                        a = 0
                    else:
                        a = randint(0,len(linenumber_list)-1)
                    del linenumber_list[a]
                    temp_line = open_keyword_file[a]
                    current_topic = getTopic(temp_line)
                    if (current_topic == '娱乐'):
                        continue

                    weibo_origin = filer.filer(temp_line).replace('/', '')
                    if (len(weibo_origin) == 0):
                        continue
                    weibo_cut = list(jieba.cut(weibo_origin))
                    weibo_cut_list = []
                    for items in weibo_cut:
                        if (items not in stop_word and len(items.strip()) > 0):
                            if (items in current_keyword_banned_list):
                                continue
                            weibo_cut_list.append(items)
                    if (len(weibo_cut_list) < 5):
                        continue
                    for current_cut in weibo_cut_list:
                        origin_text.append(current_cut)
                    used_set.add(a)
            if(len(origin_text) == 0):
                continue
            linecache.clearcache()
            print(len(origin_text))

            corpus_city[current_city_file] = count
            corpus_text.append(origin_text)
            count+=1

        del origin_text
        gc.collect()

        frequency = defaultdict(int)
        for city_file in corpus_text:
            for token in city_file:
                frequency[token] += 1
        texts = [[token for token in text if frequency[token] > 3]
                 for text in corpus_text]

        word_count_dict = corpora.Dictionary(texts)
        corpus = [word_count_dict.doc2bow(text) for text in texts]
        print('计算tfidf')
        tfidf = TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        del tfidf
        gc.collect()
        print('开始LDA模型构建')
        lda = LdaModel(corpus=corpus_tfidf, id2word=word_count_dict, num_topics=8)
        model_file = 'data/keyword_location/model/' + current_keyword + '_lda.model'

        lda.save(model_file)

        for city_name, city_index in corpus_city.items():
            city_corpus = corpus[city_index]
            doc_lda = lda.get_document_topics(city_corpus)  # 得到新文档的主题分布
            db = conntoMongoKeywordLocation()
            current_collection = db[current_keyword]
            data_toinsert = {
                'city': city_name,
                'topic_distribution': str(doc_lda)
            }
            result = current_collection.insert_one(data_toinsert)

        db = conntoMongoKeywordLocation_topic()
        current_collection = db['topic']
        data_toinsert = {
            'keyword': current_keyword,
            'all_topic': str(lda.print_topics(-1))
        }
        result = current_collection.insert_one(data_toinsert)
            #write to file
            # output_file = codecs.open('result/keyword_location/city_topic/' + current_keyword + '_city_topics.txt', 'a+', encoding='utf-8')
            # output_file.write(city_name)
            # output_file.write('\t')
            # output_file.write(str(doc_lda))
            # output_file.write('\n')
    return

# weibofilefolder = '/Volumes/chinadream/data'
# 按时间-中国梦维度-市（区）存储文件
# 按中国梦维度-市(区)存储文件
def collect_city_file(file_path_list):
    ignore_region = ['其他','海外']
    output_file_1 = '/Volumes/chinadream/keyword_location/'
    output_file_2 = '/Volumes/chinadream/time_keyword_location/'
    for current_file in file_path_list:
        print(current_file)
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')
                current_text = getText(line_section)
                current_keyword_list = getKeywordList(line_section)
                current_detailed_location = getLocation(line_section)
                current_location_list = current_detailed_location.split()
                if(len(current_location_list) == 0):
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
                for current_keyword in current_keyword_list:
                    current_out_path_1 = output_file_1 + current_keyword
                    temp1 = current_file.split('/')[-1]
                    temp2 = temp1.split('.')[0]
                    current_out_path_2_time = output_file_2 + temp2
                    if(not os.path.exists(current_out_path_1)):
                        os.mkdir(current_out_path_1)
                    if(not os.path.exists(current_out_path_2_time)):
                        os.mkdir(current_out_path_2_time)

                    keyword_location_file = codecs.open(current_out_path_1 + '/' + city + '.txt','a+',encoding='utf-8')
                    keyword_location_file.write(current_text)
                    keyword_location_file.write('\n')
                    keyword_location_file.close()

                    current_out_path_2_time_keyword = current_out_path_2_time + '/' + current_keyword

                    if(not os.path.exists(current_out_path_2_time_keyword)):
                        os.mkdir(current_out_path_2_time_keyword)
                    time_keyword_location_file = codecs.open(current_out_path_2_time_keyword + '/' + city + '.txt', 'a+', encoding='utf-8')
                    time_keyword_location_file.write(current_text)
                    time_keyword_location_file.write('\n')
                    time_keyword_location_file.close()
            e_t = time()
        print('current_file:' + current_file)
        print('current file process time: ' + str(e_t - s_t))

def statistic_keywordLocaiton_number():
    pass


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

def keyword_time(file_paht_list):
    city_list = ['北京', '天津', '内蒙古', '新疆', '河北', '甘肃', '宁夏', '山西', '陕西', '青海', '山东', '河南', '安徽', '辽宁', '吉林', '黑龙江', '江苏',
                 '浙江', '上海', '湖北', '湖南', '四川', '重庆', '贵州', '云南', '广西', '江西', '福建', '广东', '海南', '西藏', '台湾', '香港', '澳门','海外','其他']
    output_dic = {}
    output_dic = {'201409': {
        '健康': [88116, 13824, 6876, 6004, 19832, 6751, 4023, 9316, 15483, 4171, 33084, 25127, 17982, 21697, 9835, 10618,
               47041, 41010, 47815, 28618, 16985, 27373, 15393, 6632, 9237, 12248, 13709, 31086, 115449, 5469, 3341,
               6925, 10493, 3871, 33258, 73097],
        '事业有成': [383, 70, 34, 28, 73, 35, 21, 45, 78, 30, 156, 166, 94, 86, 63, 46, 380, 191, 170, 115, 81, 131, 68, 31,
                 54, 62, 54, 172, 653, 37, 20, 24, 43, 29, 135, 339],
        '发展机会': [1472, 82, 28, 27, 118, 32, 25, 55, 130, 20, 247, 200, 122, 223, 35, 49, 299, 326, 576, 237, 117, 229,
                 135, 36, 76, 69, 74, 159, 978, 33, 11, 16, 52, 14, 294, 1463],
        '生活幸福': [11551, 2168, 1117, 1064, 2999, 1798, 652, 1911, 2374, 750, 4583, 4654, 2550, 4606, 1582, 1859, 7264,
                 5190, 6389, 6166, 2474, 3393, 2205, 972, 1563, 1661, 1872, 4258, 15658, 956, 527, 966, 2109, 616, 4133,
                 8872],
        '有房': [1975, 345, 203, 220, 470, 174, 150, 214, 388, 124, 957, 601, 559, 527, 224, 307, 1024, 1401, 1189, 582,
               407, 607, 356, 175, 216, 282, 289, 651, 2875, 177, 110, 123, 203, 101, 693, 2233],
        '出名': [2842, 379, 171, 163, 567, 167, 102, 275, 425, 98, 950, 734, 545, 481, 258, 334, 1671, 1120, 1566, 738,
               480, 768, 527, 198, 294, 438, 330, 915, 3808, 171, 108, 156, 468, 144, 1741, 2681],
        '家庭幸福': [2053, 321, 166, 177, 463, 197, 100, 337, 383, 83, 802, 906, 443, 810, 251, 309, 1165, 816, 1088, 750,
                 489, 638, 305, 150, 220, 287, 303, 801, 2948, 142, 80, 139, 283, 95, 602, 1773],
        '好工作': [1270, 172, 76, 68, 241, 81, 31, 131, 239, 28, 396, 432, 260, 333, 107, 125, 668, 546, 673, 433, 388,
                424, 172, 65, 97, 156, 164, 461, 1417, 74, 30, 55, 167, 34, 460, 838],
        '平等机会': [344, 26, 13, 11, 32, 10, 11, 16, 20, 10, 82, 41, 77, 27, 14, 26, 45, 68, 116, 32, 26, 33, 23, 11, 19,
                 22, 23, 22, 103, 15, 4, 10, 13, 4, 102, 171],
        '白手起家': [450, 41, 25, 16, 78, 16, 9, 48, 89, 2, 142, 144, 70, 80, 41, 72, 190, 201, 202, 94, 60, 117, 62, 29,
                 60, 51, 55, 150, 646, 13, 3, 38, 60, 33, 185, 302],
        '成为富人': [154, 9, 7, 10, 13, 4, 2, 11, 13, 4, 40, 42, 23, 16, 7, 10, 60, 45, 72, 40, 18, 31, 23, 9, 15, 24, 18,
                 38, 150, 5, 3, 3, 12, 3, 58, 72],
        '个体自由': [714, 218, 54, 197, 84, 52, 50, 59, 71, 23, 227, 120, 493, 136, 67, 71, 416, 1113, 384, 141, 99, 145,
                 121, 45, 51, 80, 64, 106, 2293, 45, 19, 24, 49, 26, 278, 1019],
        '安享晚年': [117, 21, 5, 8, 52, 9, 4, 15, 30, 0, 39, 57, 44, 40, 16, 19, 80, 58, 62, 56, 33, 51, 26, 11, 34, 37, 61,
                 43, 310, 7, 1, 54, 17, 1, 51, 102],
        '收入足够': [25, 1, 4, 1, 3, 2, 0, 2, 4, 0, 9, 6, 3, 5, 1, 0, 9, 7, 14, 9, 1, 10, 4, 0, 0, 3, 2, 6, 31, 1, 0, 0, 3,
                 0, 9, 20],
        '个人努力': [97, 20, 15, 5, 27, 13, 3, 13, 26, 6, 42, 48, 29, 24, 18, 18, 52, 41, 55, 44, 27, 31, 18, 7, 13, 23, 20,
                 43, 144, 8, 4, 4, 17, 15, 44, 105],
        '祖国强大': [25, 4, 1, 1, 5, 2, 1, 5, 7, 0, 24, 6, 1, 9, 4, 2, 9, 10, 7, 2, 5, 12, 6, 2, 2, 2, 3, 9, 14, 3, 0, 3, 1,
                 1, 3, 20],
        '中国经济持续发展': [88, 2, 2, 0, 4, 2, 1, 1, 2, 0, 5, 5, 3, 44, 0, 0, 10, 5, 9, 4, 2, 2, 21, 1, 1, 0, 0, 2, 10, 2, 0,
                     0, 2, 0, 7, 4],
        '父辈更好': [3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 0, 2, 1, 0, 0, 0, 0, 3, 5, 0, 0, 0, 0, 0,
                 0, 1]}, '201410': {
        '健康': [251905, 43316, 22137, 18211, 56685, 28231, 13949, 26628, 40873, 15507, 81444, 72784, 53514, 60300, 29501,
               31625, 127595, 146651, 147237, 81310, 67334, 71954, 43444, 20587, 27134, 43061, 51737, 85077, 335763,
               19832, 11874, 22020, 36533, 13694, 110959, 246681],
        '出名': [5285, 759, 348, 334, 1003, 354, 187, 878, 804, 182, 1766, 1367, 1032, 1062, 651, 634, 3676, 3081, 3512,
               1521, 1081, 1735, 1159, 399, 597, 906, 841, 1750, 7778, 351, 153, 413, 1202, 227, 3874, 8553],
        '生活幸福': [56112, 16324, 12942, 11715, 20160, 12890, 10566, 13204, 16656, 9730, 26466, 25675, 19095, 23040, 13765,
                 14651, 34458, 34278, 33700, 23849, 20418, 20668, 16699, 11786, 13335, 14697, 20481, 24961, 91165,
                 11598, 9883, 11996, 18356, 10517, 22009, 69074],
        '家庭幸福': [5508, 971, 641, 633, 1443, 621, 368, 685, 1049, 342, 2230, 2377, 1395, 1620, 945, 925, 2920, 2451,
                 3083, 2061, 1607, 1631, 1113, 544, 704, 932, 1543, 2482, 9439, 491, 345, 573, 730, 449, 1798, 9198],
        '好工作': [2830, 424, 216, 218, 648, 220, 116, 337, 581, 98, 1158, 989, 694, 711, 343, 437, 2056, 3158, 1732, 1140,
                1035, 991, 593, 230, 269, 461, 514, 1055, 4532, 170, 82, 201, 1279, 135, 1110, 3277],
        '祖国强大': [62, 11, 4, 3, 12, 5, 0, 17, 10, 2, 34, 16, 10, 16, 3, 4, 20, 18, 22, 20, 6, 12, 13, 4, 6, 4, 7, 29, 46,
                 4, 2, 1, 3, 0, 17, 53],
        '个体自由': [1682, 482, 132, 147, 240, 119, 105, 160, 105, 66, 448, 370, 378, 250, 158, 200, 655, 579, 448, 306,
                 211, 264, 191, 137, 116, 155, 181, 222, 2693, 123, 77, 36, 95, 44, 275, 1549],
        '有房': [6157, 1551, 713, 588, 1403, 604, 566, 827, 1078, 446, 2350, 1961, 1664, 1658, 879, 1013, 3419, 3765,
               2918, 1657, 1323, 1825, 1149, 629, 833, 973, 1165, 1787, 9680, 516, 374, 432, 1173, 378, 1972, 8567],
        '事业有成': [941, 215, 107, 120, 255, 123, 87, 124, 184, 98, 383, 401, 249, 195, 148, 150, 604, 501, 615, 521, 285,
                 313, 229, 112, 182, 193, 352, 381, 1843, 112, 89, 106, 160, 94, 331, 1580],
        '个人努力': [272, 51, 37, 36, 85, 44, 24, 38, 55, 21, 113, 113, 91, 80, 55, 54, 142, 154, 166, 87, 63, 80, 70, 32,
                 32, 49, 106, 112, 437, 35, 21, 25, 42, 16, 76, 475],
        '白手起家': [757, 106, 57, 67, 230, 53, 31, 92, 152, 24, 364, 352, 145, 150, 84, 113, 744, 1178, 582, 216, 194, 279,
                 178, 55, 109, 168, 131, 328, 1652, 47, 16, 86, 574, 31, 387, 771],
        '发展机会': [2558, 153, 91, 71, 276, 108, 34, 143, 237, 43, 513, 444, 271, 731, 111, 133, 589, 733, 938, 442, 310,
                 468, 350, 74, 162, 157, 189, 371, 2004, 63, 38, 61, 123, 31, 630, 1113],
        '平等机会': [353, 33, 28, 18, 51, 22, 14, 37, 49, 14, 80, 233, 65, 60, 28, 45, 103, 102, 145, 65, 38, 77, 50, 20,
                 34, 50, 48, 80, 236, 30, 14, 28, 35, 24, 112, 203],
        '安享晚年': [141, 23, 9, 6, 37, 6, 4, 21, 46, 2, 61, 63, 58, 27, 17, 33, 87, 74, 102, 51, 42, 57, 34, 10, 21, 28,
                 30, 54, 209, 9, 1, 7, 14, 1, 65, 173],
        '成为富人': [305, 39, 14, 19, 83, 20, 10, 42, 44, 7, 115, 117, 60, 67, 24, 39, 158, 147, 152, 93, 60, 94, 59, 18,
                 36, 43, 50, 98, 503, 15, 4, 12, 28, 0, 91, 226],
        '中国经济持续发展': [250, 3, 0, 7, 3, 3, 0, 2, 1, 0, 8, 2, 4, 145, 2, 1, 10, 9, 16, 9, 7, 9, 32, 2, 0, 1, 0, 2, 15, 1,
                     0, 0, 2, 1, 5, 14],
        '收入足够': [111, 13, 11, 2, 5, 2, 1, 5, 7, 1, 24, 16, 15, 17, 6, 6, 37, 20, 45, 16, 11, 13, 4, 5, 5, 9, 7, 7, 71,
                 2, 0, 1, 7, 0, 45, 63],
        '父辈更好': [16, 2, 0, 4, 8, 3, 0, 3, 3, 0, 15, 8, 12, 3, 1, 9, 15, 6, 8, 15, 9, 5, 8, 1, 6, 3, 5, 7, 17, 2, 1, 2,
                 0, 0, 11, 26]}, '201411': {
        '健康': [167556, 22665, 11631, 11189, 35143, 12042, 7964, 17977, 29354, 6840, 55534, 52469, 29541, 36367, 18195,
               21063, 68304, 76311, 70394, 41867, 32294, 47690, 25011, 12753, 16869, 21136, 30720, 46610, 164878, 10510,
               5667, 11914, 14589, 6877, 160086, 128226],
        '家庭幸福': [3845, 1031, 339, 392, 2172, 417, 242, 495, 782, 215, 1449, 1173, 780, 962, 679, 534, 1609, 1559, 1551,
                 992, 771, 1118, 551, 381, 441, 571, 659, 1395, 3621, 306, 212, 353, 367, 266, 1241, 3929],
        '生活幸福': [20461, 4892, 3684, 3564, 7750, 3631, 2929, 4340, 6995, 2425, 9922, 12271, 6242, 7900, 4365, 4814,
                 12018, 12007, 10758, 7752, 6260, 11639, 5224, 3240, 4248, 4462, 5783, 8057, 24980, 3101, 2379, 3159,
                 3486, 2744, 9506, 23309],
        '好工作': [2115, 285, 146, 121, 479, 131, 60, 215, 471, 38, 792, 931, 471, 490, 209, 282, 1089, 1056, 1079, 710,
                652, 755, 343, 123, 188, 306, 295, 716, 2264, 128, 44, 99, 127, 49, 851, 1753],
        '个体自由': [399, 34, 30, 31, 43, 18, 8, 37, 46, 5, 110, 87, 108, 51, 37, 27, 144, 143, 167, 114, 52, 87, 49, 23,
                 25, 36, 43, 57, 957, 16, 7, 7, 16, 12, 89, 301],
        '出名': [3744, 558, 219, 188, 782, 211, 101, 436, 666, 67, 1483, 1188, 752, 905, 366, 554, 2265, 1911, 2437, 1034,
               733, 1438, 756, 303, 430, 640, 515, 1211, 4830, 226, 49, 197, 462, 86, 3152, 3725],
        '有房': [2935, 462, 361, 344, 813, 270, 213, 462, 830, 231, 1303, 1119, 883, 790, 527, 546, 1607, 1894, 1480, 915,
               607, 1034, 534, 288, 492, 524, 549, 985, 3864, 309, 180, 244, 341, 220, 1453, 2710],
        '发展机会': [2192, 169, 69, 59, 171, 78, 20, 123, 191, 27, 456, 528, 193, 230, 80, 117, 504, 1074, 795, 361, 199,
                 337, 206, 62, 106, 104, 167, 276, 1298, 47, 14, 35, 75, 20, 446, 731],
        '成为富人': [236, 17, 15, 13, 64, 19, 8, 28, 41, 7, 105, 98, 32, 56, 14, 31, 91, 96, 120, 65, 39, 74, 22, 9, 28, 25,
                 35, 61, 330, 6, 1, 16, 17, 4, 81, 155],
        '个人努力': [215, 32, 19, 16, 41, 11, 5, 17, 65, 9, 76, 59, 45, 50, 23, 24, 89, 103, 108, 59, 44, 63, 25, 14, 26,
                 25, 32, 71, 224, 5, 3, 15, 13, 7, 70, 224],
        '事业有成': [706, 193, 123, 140, 196, 142, 137, 187, 230, 98, 347, 344, 222, 249, 131, 188, 373, 389, 356, 277, 204,
                 303, 188, 134, 193, 148, 182, 280, 861, 130, 100, 131, 135, 115, 374, 835],
        '白手起家': [425, 48, 41, 23, 102, 24, 9, 73, 75, 7, 191, 167, 88, 99, 45, 57, 213, 359, 215, 129, 76, 173, 73, 27,
                 58, 88, 62, 136, 687, 31, 1, 9, 31, 9, 188, 328],
        '安享晚年': [90, 23, 11, 7, 20, 13, 2, 14, 29, 0, 39, 61, 20, 20, 6, 10, 61, 52, 48, 46, 24, 53, 12, 9, 17, 14, 17,
                 51, 133, 9, 2, 6, 4, 0, 45, 81],
        '平等机会': [334, 75, 59, 48, 66, 66, 53, 81, 99, 45, 114, 108, 90, 93, 63, 80, 125, 130, 172, 114, 87, 99, 86, 58,
                 57, 52, 81, 89, 242, 53, 54, 57, 53, 52, 110, 233],
        '收入足够': [61, 4, 2, 2, 11, 3, 2, 3, 8, 1, 18, 14, 7, 16, 3, 10, 17, 29, 69, 8, 7, 15, 10, 1, 4, 5, 6, 19, 67, 2,
                 0, 0, 5, 0, 26, 49],
        '中国经济持续发展': [106, 1, 2, 1, 0, 1, 0, 0, 2, 0, 2, 4, 1, 20, 2, 1, 9, 8, 14, 2, 3, 1, 3, 0, 1, 0, 1, 1, 8, 2, 0, 0,
                     3, 1, 1, 11],
        '祖国强大': [46, 5, 0, 2, 17, 5, 0, 4, 12, 0, 32, 19, 13, 14, 8, 7, 35, 17, 28, 7, 10, 21, 19, 4, 4, 7, 5, 18, 40,
                 2, 0, 0, 2, 0, 29, 56],
        '父辈更好': [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 5, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0,
                 1, 3]}, '201412': {
        '健康': [177769, 30965, 16472, 13489, 52639, 14937, 10009, 25062, 45506, 7248, 85431, 64257, 41613, 54966, 23323,
               29335, 97564, 96781, 99370, 53518, 41285, 65271, 34538, 15499, 21096, 30053, 40895, 61649, 237938, 12448,
               6019, 12836, 27855, 6704, 82145, 226782],
        '生活幸福': [25836, 4374, 2756, 2318, 7947, 2902, 1503, 3646, 8702, 1174, 11763, 10388, 7048, 9329, 3478, 4187,
                 13589, 11238, 14523, 8792, 5746, 8095, 4427, 2186, 3400, 3998, 5232, 8520, 33950, 1885, 1161, 1985,
                 2611, 1439, 8778, 48114],
        '家庭幸福': [4526, 751, 481, 407, 1901, 389, 256, 665, 1464, 195, 2047, 1848, 1102, 1386, 574, 685, 2295, 1926,
                 2080, 1260, 1070, 1445, 800, 404, 523, 741, 892, 1874, 6692, 354, 182, 386, 492, 264, 1668, 8191],
        '事业有成': [860, 196, 89, 87, 228, 74, 49, 126, 321, 42, 424, 476, 237, 272, 152, 159, 542, 442, 442, 268, 210,
                 280, 163, 71, 119, 160, 202, 360, 1510, 77, 32, 68, 102, 64, 385, 1737],
        '出名': [5040, 765, 368, 340, 1033, 366, 208, 528, 1027, 143, 2030, 1587, 1001, 1228, 597, 703, 2816, 2496, 3111,
               1332, 950, 1829, 907, 459, 612, 828, 674, 1592, 5850, 305, 143, 309, 591, 167, 4253, 5296],
        '白手起家': [461, 79, 47, 24, 132, 28, 15, 88, 97, 6, 457, 201, 104, 124, 44, 86, 242, 346, 231, 133, 102, 173, 89,
                 35, 56, 55, 193, 162, 752, 52, 3, 21, 47, 12, 254, 689],
        '好工作': [2934, 462, 218, 189, 657, 164, 180, 373, 761, 70, 1181, 1034, 663, 724, 297, 408, 1595, 1364, 1526,
                1029, 1045, 986, 556, 195, 282, 446, 487, 940, 3573, 152, 55, 143, 175, 74, 1140, 2895],
        '安享晚年': [177, 29, 15, 21, 64, 9, 1, 17, 55, 3, 104, 84, 42, 46, 24, 27, 113, 77, 96, 63, 51, 65, 31, 20, 26, 43,
                 23, 48, 189, 9, 6, 8, 9, 2, 76, 169],
        '发展机会': [2285, 206, 101, 67, 322, 101, 55, 136, 237, 37, 533, 425, 188, 550, 104, 134, 622, 700, 942, 325, 198,
                 366, 211, 82, 138, 172, 128, 326, 1568, 96, 33, 67, 84, 37, 452, 952],
        '父辈更好': [7, 4, 1, 0, 1, 0, 0, 0, 0, 0, 4, 1, 1, 1, 2, 2, 2, 2, 2, 4, 2, 6, 11, 0, 1, 1, 0, 0, 12, 0, 0, 1, 0, 0,
                 2, 1],
        '有房': [3352, 507, 284, 212, 785, 255, 189, 402, 881, 177, 1206, 1002, 993, 908, 395, 510, 1543, 2018, 1802, 869,
               597, 941, 523, 243, 457, 473, 483, 899, 4898, 269, 123, 175, 263, 118, 1210, 4666],
        '收入足够': [71, 6, 4, 3, 11, 4, 0, 3, 8, 1, 16, 5, 13, 15, 8, 4, 22, 16, 46, 13, 4, 18, 5, 1, 6, 3, 5, 13, 62, 9,
                 0, 2, 4, 0, 32, 37],
        '平等机会': [543, 43, 13, 25, 38, 27, 10, 90, 82, 70, 94, 91, 123, 40, 23, 16, 160, 105, 210, 66, 51, 68, 43, 38,
                 30, 31, 37, 60, 273, 21, 13, 6, 24, 81, 114, 278],
        '成为富人': [218, 33, 17, 21, 63, 29, 7, 34, 57, 16, 121, 101, 34, 69, 15, 29, 102, 110, 117, 65, 44, 75, 39, 23,
                 31, 35, 30, 47, 266, 11, 8, 7, 12, 1, 82, 184],
        '祖国强大': [35, 4, 4, 9, 17, 7, 0, 5, 12, 1, 17, 39, 12, 12, 5, 11, 42, 19, 18, 17, 7, 13, 14, 7, 1, 1, 5, 73, 20,
                 2, 0, 0, 2, 1, 21, 43],
        '个体自由': [358, 36, 25, 17, 37, 23, 22, 19, 39, 10, 63, 45, 154, 48, 17, 15, 102, 117, 134, 87, 44, 57, 22, 17,
                 14, 31, 26, 44, 901, 19, 6, 9, 16, 2, 58, 486],
        '个人努力': [231, 35, 21, 15, 44, 22, 8, 27, 61, 11, 85, 77, 43, 45, 31, 35, 119, 90, 108, 72, 91, 75, 48, 13, 31,
                 33, 52, 74, 241, 12, 6, 15, 25, 14, 117, 429],
        '中国经济持续发展': [111, 3, 3, 2, 5, 0, 0, 2, 5, 0, 10, 7, 0, 38, 3, 1, 6, 8, 15, 3, 5, 5, 1, 5, 6, 0, 1, 6, 19, 0, 2,
                     1, 1, 0, 9, 28]}, '201501': {
        '健康': [190821, 36183, 21241, 18186, 54113, 18163, 16783, 29770, 47761, 10644, 95582, 67832, 51121, 64036, 30977,
               34458, 107652, 103784, 108550, 58899, 43536, 75855, 39855, 19095, 28794, 34215, 39565, 63008, 292192,
               17788, 10986, 19845, 22935, 10470, 91203, 241182],
        '有房': [3580, 616, 435, 406, 925, 395, 292, 574, 1003, 400, 1561, 1286, 1179, 1228, 564, 704, 1763, 2670, 1889,
               1078, 797, 1420, 679, 380, 531, 651, 708, 1109, 7636, 409, 257, 317, 385, 220, 1918, 5273],
        '家庭幸福': [5113, 1001, 626, 574, 1452, 583, 442, 830, 1353, 362, 3226, 2474, 1239, 1585, 811, 955, 2790, 2268,
                 2862, 1519, 1395, 2365, 920, 595, 677, 883, 992, 1960, 8473, 660, 362, 450, 624, 373, 1825, 8687],
        '生活幸福': [27985, 5363, 3932, 3622, 7816, 3727, 2801, 4725, 8322, 2563, 13121, 10629, 7760, 12621, 4736, 5491,
                 13619, 13494, 13636, 9823, 7297, 11908, 5514, 3233, 4296, 5208, 6447, 8932, 45868, 3050, 2324, 2727,
                 3253, 1972, 9179, 49659],
        '事业有成': [1312, 248, 152, 129, 303, 142, 87, 199, 346, 95, 565, 552, 402, 386, 228, 212, 600, 593, 648, 339, 290,
                 564, 245, 134, 179, 224, 269, 480, 2220, 128, 78, 117, 133, 85, 567, 1950],
        '好工作': [3065, 520, 349, 323, 786, 256, 193, 378, 846, 128, 1268, 1290, 725, 816, 372, 449, 1734, 1626, 1651,
                1008, 1007, 1313, 603, 267, 363, 577, 519, 1064, 5709, 212, 109, 207, 259, 127, 1291, 3098],
        '出名': [6084, 1234, 676, 587, 1538, 575, 393, 873, 1427, 328, 2656, 1946, 1351, 1783, 934, 1227, 3679, 3077,
               4170, 1965, 1364, 3123, 2114, 679, 860, 1163, 1189, 2162, 7253, 499, 332, 540, 876, 352, 5196, 6538],
        '个人努力': [241, 40, 25, 16, 58, 30, 23, 35, 60, 10, 100, 69, 79, 75, 40, 57, 103, 124, 106, 77, 38, 86, 70, 28,
                 39, 41, 73, 76, 265, 29, 14, 20, 30, 21, 101, 402],
        '白手起家': [1169, 95, 48, 56, 175, 62, 46, 115, 140, 41, 357, 189, 128, 180, 111, 100, 269, 381, 305, 178, 152,
                 218, 114, 59, 89, 103, 2075, 186, 887, 56, 32, 40, 76, 22, 263, 602],
        '发展机会': [2296, 296, 190, 137, 408, 154, 143, 235, 338, 123, 611, 470, 271, 1150, 227, 189, 624, 575, 855, 401,
                 324, 451, 285, 150, 243, 362, 225, 378, 1818, 148, 109, 155, 191, 107, 611, 892],
        '个体自由': [451, 69, 43, 43, 68, 45, 30, 72, 91, 38, 139, 106, 252, 95, 48, 49, 170, 341, 219, 113, 94, 165, 80,
                 38, 61, 68, 63, 97, 2364, 43, 23, 25, 52, 35, 167, 1086],
        '祖国强大': [28, 0, 0, 5, 11, 1, 2, 9, 6, 0, 19, 6, 4, 13, 5, 7, 18, 13, 16, 6, 6, 7, 10, 6, 3, 2, 4, 51, 32, 0, 1,
                 2, 2, 0, 21, 31],
        '安享晚年': [244, 40, 23, 17, 51, 16, 16, 32, 71, 8, 119, 113, 55, 49, 29, 34, 134, 123, 142, 69, 42, 100, 40, 19,
                 20, 26, 43, 66, 220, 17, 14, 14, 15, 11, 94, 206],
        '平等机会': [2753, 56, 31, 17, 52, 21, 13, 63, 132, 15, 92, 104, 1560, 32, 37, 25, 97, 87, 208, 54, 39, 61, 39, 12,
                 32, 32, 28, 152, 281, 431, 12, 15, 14, 11, 425, 226],
        '收入足够': [71, 12, 8, 6, 12, 5, 11, 13, 14, 4, 23, 39, 13, 16, 8, 12, 32, 35, 35, 19, 8, 19, 13, 6, 6, 13, 9, 15,
                 80, 7, 2, 8, 9, 1, 24, 34],
        '成为富人': [215, 25, 24, 27, 75, 19, 11, 42, 52, 13, 117, 89, 40, 63, 26, 35, 129, 85, 116, 79, 55, 77, 33, 27, 27,
                 29, 38, 66, 235, 24, 13, 9, 25, 6, 89, 134],
        '父辈更好': [3, 0, 2, 0, 2, 0, 1, 3, 2, 1, 3, 0, 0, 2, 0, 0, 2, 2, 4, 1, 1, 3, 2, 1, 0, 4, 0, 0, 4, 1, 1, 1, 1, 2,
                 3, 3],
        '中国经济持续发展': [68, 2, 1, 4, 1, 0, 1, 1, 5, 0, 7, 3, 2, 14, 0, 1, 10, 7, 3, 5, 3, 9, 2, 1, 2, 0, 1, 8, 11, 1, 0, 0,
                     4, 3, 1, 9]}, '201502': {
        '健康': [150723, 43816, 32105, 29236, 61802, 38664, 24466, 38213, 49989, 23315, 85269, 67532, 46995, 67368, 38131,
               49275, 106820, 105660, 94904, 56932, 47286, 66786, 46767, 34353, 35642, 50667, 44703, 61146, 236806,
               32847, 24461, 28466, 32132, 22533, 85481, 215249],
        '生活幸福': [23778, 7417, 5829, 5443, 8979, 6124, 6864, 6611, 8501, 4851, 12357, 11389, 8082, 12924, 6532, 7297,
                 13397, 18528, 12948, 13187, 7712, 9838, 6938, 6046, 6298, 7026, 6988, 9415, 32435, 5360, 4834, 4880,
                 5188, 3744, 9610, 43606],
        '收入足够': [55, 15, 14, 12, 23, 18, 10, 14, 19, 5, 27, 22, 17, 23, 14, 15, 30, 31, 26, 16, 22, 29, 18, 20, 17, 19,
                 16, 27, 57, 11, 11, 12, 17, 15, 30, 23],
        '出名': [4881, 1502, 1161, 1092, 1796, 1152, 930, 1300, 1625, 932, 2656, 2044, 1726, 1942, 1416, 1497, 3234, 2971,
               3563, 2012, 1638, 2508, 1737, 1207, 1400, 1598, 1414, 2234, 5660, 1041, 914, 956, 1157, 795, 4064, 5310],
        '家庭幸福': [5474, 1532, 1192, 1112, 2048, 1120, 901, 1390, 1789, 859, 3083, 2681, 1688, 2199, 1325, 1445, 3401,
                 3063, 3052, 2140, 1839, 2431, 1593, 1082, 1203, 1535, 1489, 2323, 10419, 1004, 828, 950, 1044, 705,
                 2455, 7022],
        '安享晚年': [133, 37, 28, 12, 41, 24, 27, 20, 49, 19, 66, 55, 39, 41, 30, 31, 81, 73, 80, 39, 41, 91, 32, 34, 32,
                 28, 35, 29, 146, 25, 20, 16, 23, 19, 60, 85],
        '白手起家': [486, 146, 112, 114, 203, 112, 105, 132, 164, 84, 297, 256, 185, 208, 125, 141, 275, 311, 298, 186, 171,
                 250, 165, 118, 136, 161, 290, 211, 729, 132, 98, 114, 104, 86, 228, 488],
        '有房': [3249, 1030, 784, 791, 1281, 840, 740, 1026, 1194, 757, 1726, 1714, 1289, 1351, 974, 1042, 2102, 5545,
               1971, 1281, 1001, 1481, 1032, 804, 894, 1001, 1027, 1348, 5686, 761, 665, 658, 665, 538, 1801, 6141],
        '好工作': [2248, 583, 381, 383, 760, 346, 284, 498, 788, 264, 1159, 994, 712, 877, 465, 580, 1577, 1406, 1482,
                1012, 1011, 1059, 655, 388, 427, 729, 620, 944, 3072, 313, 264, 299, 334, 218, 1298, 3136],
        '发展机会': [1821, 482, 430, 375, 478, 392, 402, 506, 532, 387, 726, 648, 491, 1163, 491, 452, 853, 701, 918, 595,
                 506, 662, 505, 431, 464, 772, 496, 535, 1707, 400, 382, 404, 467, 406, 808, 744],
        '事业有成': [1452, 454, 314, 259, 614, 282, 215, 386, 459, 195, 763, 873, 476, 611, 359, 412, 1044, 864, 924, 611,
                 463, 641, 360, 297, 331, 383, 398, 747, 2272, 236, 205, 215, 238, 131, 705, 1865],
        '平等机会': [460, 106, 38, 38, 51, 46, 35, 46, 61, 45, 95, 64, 1896, 60, 52, 58, 104, 67, 124, 74, 57, 84, 53, 67,
                 46, 57, 55, 67, 180, 45, 46, 41, 49, 42, 288, 211],
        '个体自由': [415, 94, 68, 71, 97, 76, 69, 82, 99, 69, 135, 105, 168, 105, 83, 100, 245, 1818, 285, 123, 115, 145,
                 94, 76, 78, 106, 95, 111, 1448, 80, 63, 62, 92, 63, 153, 619],
        '个人努力': [202, 47, 50, 35, 60, 42, 29, 41, 71, 34, 119, 101, 64, 74, 51, 52, 126, 135, 107, 69, 64, 68, 61, 33,
                 42, 49, 57, 78, 218, 46, 36, 42, 44, 35, 97, 269],
        '中国经济持续发展': [66, 4, 1, 3, 1, 1, 1, 6, 2, 6, 10, 6, 6, 21, 6, 0, 12, 2, 19, 1, 5, 2, 7, 2, 3, 2, 3, 6, 16, 3, 1,
                     5, 1, 3, 5, 8],
        '祖国强大': [33, 8, 3, 4, 8, 6, 4, 8, 9, 2, 15, 13, 4, 11, 1, 5, 16, 11, 14, 9, 6, 11, 4, 3, 3, 3, 2, 11, 26, 2, 0,
                 5, 7, 4, 24, 31],
        '成为富人': [202, 49, 44, 38, 86, 42, 29, 40, 54, 32, 115, 86, 71, 58, 49, 65, 115, 69, 124, 79, 63, 73, 58, 43, 38,
                 46, 39, 60, 179, 28, 25, 25, 44, 33, 71, 121],
        '父辈更好': [5, 2, 1, 0, 6, 3, 1, 1, 5, 5, 4, 2, 1, 2, 2, 3, 4, 3, 7, 3, 2, 8, 2, 3, 3, 1, 2, 4, 9, 4, 1, 5, 2, 1,
                 2, 2]}, '201503': {
        '出名': [4373, 1239, 915, 916, 1373, 876, 859, 1086, 1233, 815, 2113, 1547, 1295, 1574, 1156, 1205, 2617, 2495,
               3382, 1716, 1408, 2098, 1379, 1008, 1131, 1290, 1084, 1761, 4729, 896, 799, 883, 1017, 711, 3859, 4730],
        '健康': [120690, 33918, 27048, 24313, 43061, 29413, 22714, 30165, 41380, 21982, 70104, 54377, 36076, 50148, 43556,
               40869, 74446, 78200, 70260, 46259, 37734, 54992, 37523, 25130, 32403, 37388, 36754, 51714, 168470, 28688,
               18478, 21558, 26840, 16993, 74393, 193603],
        '生活幸福': [22451, 6363, 5190, 4683, 8026, 5315, 6635, 5848, 7610, 4749, 10919, 10147, 7631, 10286, 6085, 6251,
                 12115, 16867, 11587, 12677, 7046, 9413, 6627, 4993, 5887, 6253, 7157, 8445, 26298, 4930, 3921, 4514,
                 4838, 3325, 10252, 70825],
        '有房': [3723, 836, 731, 682, 1119, 717, 622, 843, 1039, 744, 1422, 1411, 1284, 1223, 799, 945, 2149, 4477, 2291,
               1167, 914, 1301, 939, 708, 802, 947, 926, 1264, 4857, 658, 573, 613, 669, 480, 1823, 8151],
        '事业有成': [1021, 343, 263, 172, 371, 308, 239, 260, 338, 233, 426, 497, 366, 380, 262, 334, 804, 472, 527, 381,
                 359, 443, 324, 276, 289, 321, 305, 471, 1181, 296, 157, 182, 172, 152, 457, 1523],
        '家庭幸福': [4071, 1243, 925, 893, 1400, 882, 819, 1085, 1324, 850, 1996, 1842, 1275, 1526, 996, 1092, 2346, 2143,
                 2147, 1506, 1208, 1697, 1129, 873, 1011, 1193, 1316, 1512, 4952, 889, 710, 817, 898, 606, 2045, 7267],
        '好工作': [1898, 461, 325, 298, 699, 308, 236, 429, 602, 245, 1036, 830, 602, 693, 412, 486, 1175, 1216, 1144, 863,
                1142, 843, 533, 325, 385, 521, 504, 866, 2335, 267, 237, 266, 315, 215, 1131, 3702],
        '安享晚年': [92, 34, 25, 24, 46, 28, 21, 33, 39, 13, 57, 61, 40, 40, 28, 20, 79, 57, 66, 57, 32, 51, 24, 16, 32, 65,
                 22, 39, 141, 13, 14, 22, 26, 17, 67, 79],
        '白手起家': [678, 249, 427, 130, 351, 110, 284, 162, 178, 90, 397, 351, 271, 556, 287, 400, 1031, 399, 421, 248,
                 165, 262, 126, 214, 502, 171, 316, 430, 811, 105, 371, 78, 131, 64, 326, 747],
        '发展机会': [1474, 421, 372, 396, 478, 413, 350, 414, 487, 355, 714, 611, 483, 1270, 410, 409, 740, 670, 929, 573,
                 492, 731, 492, 381, 471, 599, 439, 534, 1615, 380, 336, 314, 381, 379, 764, 1139],
        '平等机会': [299, 42, 43, 242, 134, 38, 41, 45, 55, 50, 104, 100, 155, 60, 40, 52, 91, 188, 159, 65, 56, 97, 65, 43,
                 46, 217, 43, 58, 240, 58, 35, 57, 33, 33, 386, 261],
        '中国经济持续发展': [19, 3, 4, 3, 7, 3, 5, 2, 3, 2, 6, 3, 3, 25, 3, 1, 6, 4, 9, 8, 3, 3, 2, 1, 1, 0, 4, 2, 6, 1, 3, 1,
                     1, 2, 6, 14],
        '成为富人': [108, 29, 31, 29, 38, 25, 25, 26, 38, 29, 64, 49, 40, 56, 37, 44, 79, 43, 85, 67, 41, 43, 35, 32, 42,
                 38, 35, 41, 112, 33, 24, 22, 20, 16, 73, 95],
        '个人努力': [171, 41, 40, 33, 52, 31, 26, 36, 43, 36, 71, 65, 45, 69, 39, 43, 499, 106, 85, 62, 41, 70, 46, 37, 49,
                 54, 62, 71, 149, 26, 32, 37, 25, 78, 105, 355],
        '个体自由': [476, 98, 68, 55, 115, 81, 70, 72, 88, 51, 139, 116, 162, 122, 91, 97, 292, 1246, 280, 119, 98, 149,
                 173, 79, 70, 100, 95, 117, 1181, 66, 50, 73, 71, 46, 168, 663],
        '收入足够': [86, 19, 9, 10, 17, 10, 11, 26, 14, 11, 26, 16, 10, 25, 13, 20, 269, 33, 31, 19, 22, 23, 14, 14, 9, 20,
                 12, 26, 92, 17, 19, 12, 32, 10, 38, 51],
        '父辈更好': [5, 1, 0, 0, 1, 2, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 1, 3, 3, 3, 0, 2, 0, 0, 2, 1, 0, 1, 3, 0, 0, 2, 0, 0,
                 3, 6],
        '祖国强大': [31, 9, 5, 9, 16, 6, 1, 4, 5, 0, 32, 17, 11, 16, 2, 8, 26, 16, 15, 17, 11, 10, 12, 5, 6, 6, 8, 19, 44,
                 5, 2, 1, 3, 4, 25, 33]}, '201504': {
        '健康': [110569, 29454, 22676, 18614, 39969, 22686, 17063, 27208, 34608, 16862, 59609, 51107, 33261, 46062, 26107,
               31532, 68791, 80182, 68608, 47829, 36078, 48894, 37201, 22802, 26992, 30270, 30244, 47245, 173146, 19671,
               14410, 17491, 24421, 12159, 66006, 260336],
        '出名': [4076, 981, 753, 726, 1139, 780, 620, 845, 1086, 634, 1926, 1383, 1277, 1275, 864, 995, 2480, 2358, 2752,
               1603, 1265, 1926, 1256, 818, 941, 1064, 922, 1728, 5516, 697, 509, 711, 801, 548, 3398, 5753],
        '生活幸福': [20037, 5759, 4752, 4252, 7333, 4727, 4493, 5056, 6788, 3957, 10519, 13087, 7039, 9173, 5260, 5605,
                 11722, 15103, 11290, 14316, 6672, 8398, 6220, 4397, 5286, 5565, 6226, 7901, 23747, 4241, 3170, 3512,
                 3838, 2815, 9653, 66602],
        '家庭幸福': [3210, 948, 820, 702, 1197, 776, 665, 865, 1109, 630, 1741, 1477, 1150, 1333, 883, 932, 1950, 2135,
                 2054, 1468, 1191, 1345, 967, 693, 872, 975, 1003, 1229, 4411, 702, 515, 618, 661, 485, 1721, 8499],
        '好工作': [1913, 414, 298, 259, 530, 305, 207, 395, 545, 217, 895, 783, 595, 640, 378, 398, 1254, 1274, 1189, 915,
                1010, 812, 492, 273, 368, 445, 468, 760, 2431, 290, 181, 244, 285, 172, 1216, 4672],
        '有房': [4027, 679, 506, 446, 926, 464, 412, 611, 948, 484, 1303, 1134, 978, 1125, 616, 647, 1653, 3128, 2061,
               1050, 799, 1123, 883, 479, 633, 707, 611, 973, 4324, 418, 305, 411, 460, 273, 1558, 9662],
        '发展机会': [1218, 355, 251, 318, 434, 288, 277, 300, 376, 274, 614, 477, 415, 1264, 298, 300, 590, 584, 772, 539,
                 376, 461, 400, 312, 324, 369, 399, 535, 2153, 294, 236, 265, 283, 225, 580, 2056],
        '白手起家': [474, 160, 98, 87, 211, 137, 151, 139, 170, 48, 293, 314, 140, 249, 2202, 169, 355, 401, 463, 288, 151,
                 205, 151, 73, 93, 150, 129, 176, 897, 58, 34, 53, 75, 40, 286, 2556],
        '平等机会': [177, 42, 33, 112, 59, 63, 28, 27, 68, 30, 85, 74, 78, 49, 30, 94, 90, 144, 125, 52, 61, 64, 117, 35,
                 40, 36, 89, 67, 222, 34, 27, 30, 23, 31, 163, 220],
        '事业有成': [989, 288, 265, 168, 327, 298, 249, 277, 325, 238, 418, 503, 335, 376, 282, 315, 472, 473, 569, 419,
                 355, 425, 319, 280, 287, 310, 322, 405, 1224, 260, 136, 144, 147, 101, 416, 2013],
        '个体自由': [608, 89, 78, 61, 91, 70, 56, 92, 107, 62, 135, 129, 187, 124, 85, 88, 169, 568, 368, 118, 98, 150, 205,
                 88, 92, 89, 78, 103, 1048, 63, 60, 56, 117, 49, 169, 1278],
        '收入足够': [57, 18, 12, 13, 16, 7, 8, 11, 11, 6, 25, 27, 13, 16, 10, 7, 549, 33, 37, 22, 14, 17, 12, 9, 11, 17, 15,
                 25, 91, 24, 24, 10, 18, 11, 27, 50],
        '个人努力': [339, 54, 40, 36, 66, 30, 37, 61, 80, 33, 118, 107, 74, 89, 47, 45, 152, 116, 110, 76, 66, 84, 61, 37,
                 51, 53, 55, 90, 267, 37, 24, 33, 43, 310, 151, 392],
        '祖国强大': [107, 19, 10, 10, 18, 10, 4, 11, 29, 1, 45, 33, 19, 32, 12, 10, 59, 40, 60, 23, 20, 28, 38, 10, 5, 14,
                 23, 41, 80, 11, 2, 2, 6, 2, 72, 98],
        '成为富人': [160, 17, 14, 22, 38, 32, 17, 27, 46, 19, 75, 67, 56, 51, 30, 54, 100, 83, 85, 56, 47, 81, 33, 29, 36,
                 33, 37, 57, 212, 20, 14, 14, 21, 19, 80, 160],
        '安享晚年': [85, 23, 15, 12, 30, 10, 3, 26, 48, 4, 52, 29, 30, 32, 23, 17, 64, 64, 67, 43, 41, 48, 19, 14, 17, 35,
                 19, 36, 133, 14, 6, 13, 13, 4, 75, 94],
        '中国经济持续发展': [23, 0, 0, 1, 0, 0, 1, 0, 3, 1, 6, 0, 2, 25, 2, 1, 3, 3, 7, 4, 1, 2, 0, 1, 1, 2, 1, 0, 7, 0, 0, 0,
                     0, 0, 2, 10],
        '父辈更好': [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 2, 0, 0, 0, 2, 3, 1, 0, 3, 0, 0, 1, 0, 0, 2, 2, 2, 0, 0, 0, 0,
                 0, 1]}, '201505': {
        '健康': [132600, 40216, 30402, 25754, 55060, 34115, 30749, 37982, 49476, 26626, 79114, 67025, 49652, 57198, 36446,
               39781, 87815, 110156, 89014, 60376, 48868, 66784, 43991, 32214, 39067, 42238, 43101, 64046, 284304,
               30786, 20189, 23784, 27889, 21525, 73838, 311976],
        '家庭幸福': [3508, 1255, 952, 794, 1459, 984, 848, 1036, 1436, 794, 2105, 1940, 1435, 1607, 1029, 1140, 2345, 2245,
                 2319, 1853, 1484, 1742, 1227, 922, 1161, 1241, 1278, 1731, 5045, 931, 612, 686, 795, 603, 1704, 8192],
        '生活幸福': [20488, 7118, 6154, 4845, 8641, 6075, 5443, 6501, 8356, 5285, 12255, 11058, 8697, 9548, 6789, 7212,
                 13192, 20340, 14862, 11516, 8238, 9912, 7488, 5830, 6581, 6982, 7177, 9560, 27743, 5931, 4162, 4409,
                 4614, 3793, 9049, 58706],
        '好工作': [1894, 554, 374, 350, 678, 393, 302, 473, 674, 227, 1109, 945, 650, 758, 399, 494, 1401, 1311, 1356,
                1011, 1150, 940, 663, 390, 437, 629, 540, 887, 2573, 364, 230, 299, 353, 235, 1176, 4897],
        '出名': [4023, 1345, 878, 843, 1383, 897, 761, 1082, 1325, 780, 2226, 1715, 1480, 1608, 1045, 1213, 2681, 2684,
               3055, 1780, 1522, 2357, 1463, 1038, 1144, 1265, 1222, 1998, 6207, 928, 731, 889, 1115, 732, 3714, 5710],
        '有房': [3160, 779, 612, 521, 1137, 588, 539, 703, 902, 566, 1454, 1570, 1726, 1164, 752, 828, 2299, 7689, 3232,
               1271, 980, 1405, 926, 668, 735, 911, 841, 1242, 5246, 608, 415, 517, 508, 364, 1613, 9208],
        '个人努力': [210, 62, 67, 44, 85, 52, 39, 56, 90, 45, 138, 116, 94, 88, 72, 66, 145, 141, 116, 102, 62, 100, 66, 52,
                 77, 75, 90, 103, 239, 46, 32, 38, 44, 33, 128, 375],
        '发展机会': [2524, 523, 4131, 349, 585, 354, 348, 457, 460, 358, 723, 673, 472, 1132, 408, 425, 702, 824, 934, 882,
                 484, 596, 497, 375, 398, 471, 414, 563, 2433, 347, 307, 403, 343, 302, 621, 1760],
        '事业有成': [951, 413, 294, 192, 402, 403, 291, 357, 439, 303, 574, 685, 407, 496, 319, 374, 682, 678, 659, 585,
                 467, 497, 387, 354, 347, 343, 400, 586, 1430, 348, 150, 176, 209, 143, 445, 1644],
        '个体自由': [558, 131, 115, 85, 136, 108, 81, 72, 119, 66, 184, 175, 283, 149, 133, 123, 512, 3427, 1105, 186, 170,
                 201, 156, 120, 117, 111, 169, 177, 1395, 94, 70, 68, 115, 60, 208, 1287],
        '平等机会': [172, 51, 42, 74, 77, 40, 29, 52, 71, 32, 92, 72, 282, 62, 37, 54, 90, 86, 124, 141, 58, 98, 55, 48, 53,
                 52, 50, 76, 192, 43, 35, 38, 41, 42, 109, 197],
        '白手起家': [718, 160, 136, 124, 325, 114, 67, 181, 259, 59, 428, 449, 251, 383, 157, 243, 444, 433, 380, 331, 232,
                 326, 187, 110, 139, 188, 145, 298, 1115, 124, 67, 62, 100, 57, 368, 1080],
        '收入足够': [45, 14, 14, 10, 16, 10, 9, 14, 20, 12, 30, 19, 13, 20, 13, 15, 21, 23, 29, 16, 17, 22, 15, 9, 14, 18,
                 18, 17, 51, 15, 12, 9, 12, 9, 20, 18],
        '成为富人': [150, 49, 39, 38, 41, 21, 27, 30, 69, 33, 66, 94, 52, 52, 38, 34, 83, 72, 87, 60, 48, 64, 45, 25, 41,
                 37, 31, 55, 240, 31, 15, 23, 28, 16, 54, 101],
        '安享晚年': [77, 21, 10, 9, 37, 11, 8, 18, 35, 7, 41, 75, 35, 29, 11, 22, 71, 50, 53, 51, 31, 50, 32, 8, 24, 43, 17,
                 30, 165, 10, 5, 7, 11, 6, 48, 87],
        '中国经济持续发展': [18, 2, 0, 0, 2, 1, 0, 0, 2, 1, 2, 4, 0, 21, 0, 0, 5, 3, 6, 2, 2, 3, 2, 0, 2, 0, 0, 2, 11, 1, 0, 1,
                     0, 0, 3, 9],
        '祖国强大': [48, 7, 9, 9, 6, 6, 6, 10, 11, 2, 17, 10, 14, 9, 8, 2, 16, 25, 19, 10, 11, 17, 26, 1, 14, 5, 3, 13, 26,
                 5, 5, 6, 7, 1, 35, 26],
        '父辈更好': [1, 0, 1, 0, 1, 0, 0, 1, 4, 0, 4, 2, 0, 1, 0, 0, 1, 4, 2, 0, 1, 0, 1, 0, 1, 0, 0, 1, 5, 0, 0, 1, 1, 0,
                 4, 4]}, '201506': {
        '健康': [112411, 35102, 28302, 23042, 46740, 28586, 23576, 33579, 44410, 21948, 68350, 58486, 41887, 50044, 36849,
               35027, 78538, 82811, 76949, 51132, 43433, 57845, 39603, 29475, 32239, 37984, 43346, 56403, 197958, 25972,
               20686, 21771, 24603, 17366, 64879, 208058],
        '生活幸福': [17298, 6407, 5466, 4086, 8124, 5453, 4749, 5891, 7472, 4672, 10612, 9596, 7480, 9155, 6005, 6372,
                 11768, 13135, 10796, 8757, 7263, 8948, 6697, 5356, 6181, 6286, 6441, 8552, 26941, 5206, 3469, 3804,
                 4017, 3257, 8444, 34245],
        '发展机会': [1197, 373, 281, 253, 407, 301, 281, 308, 445, 259, 591, 486, 360, 458, 308, 317, 603, 1126, 778, 470,
                 401, 481, 394, 282, 305, 355, 349, 453, 2000, 271, 227, 267, 301, 242, 589, 1677],
        '好工作': [1596, 450, 316, 318, 615, 304, 198, 387, 554, 210, 972, 878, 559, 623, 353, 414, 1199, 1140, 1162, 812,
                1028, 828, 507, 315, 405, 512, 463, 772, 2336, 312, 196, 265, 284, 176, 1061, 2726],
        '家庭幸福': [3073, 1145, 957, 702, 1218, 864, 792, 972, 1230, 730, 1927, 1968, 1190, 1418, 1061, 1231, 2064, 1882,
                 2019, 1531, 1359, 1615, 1189, 901, 1065, 1090, 1116, 1555, 4658, 882, 540, 649, 711, 561, 1551, 6207],
        '事业有成': [814, 277, 204, 160, 295, 229, 140, 229, 329, 141, 470, 478, 303, 374, 227, 255, 637, 596, 494, 434,
                 346, 414, 330, 216, 233, 342, 272, 444, 1297, 192, 124, 175, 177, 122, 630, 1963],
        '有房': [3035, 724, 518, 443, 939, 441, 402, 596, 799, 488, 1368, 1166, 1118, 1025, 601, 722, 2127, 4101, 2342,
               1108, 886, 1238, 808, 527, 638, 834, 833, 1215, 6634, 470, 365, 362, 466, 311, 1733, 4395],
        '个人努力': [212, 80, 65, 41, 72, 49, 46, 73, 72, 45, 114, 113, 70, 79, 50, 86, 129, 104, 112, 85, 76, 97, 67, 57,
                 55, 65, 69, 78, 248, 57, 29, 39, 52, 32, 122, 354],
        '出名': [3948, 1123, 840, 741, 1436, 814, 631, 1039, 1278, 643, 2187, 1634, 1368, 1575, 947, 1160, 2849, 2625,
               2993, 1717, 1411, 2099, 1932, 899, 1071, 1250, 1240, 1758, 6007, 816, 601, 776, 979, 632, 3821, 5526],
        '白手起家': [431, 111, 90, 95, 192, 77, 57, 132, 172, 37, 285, 280, 149, 208, 139, 140, 340, 489, 248, 217, 189,
                 213, 117, 78, 97, 127, 120, 221, 897, 60, 32, 54, 92, 42, 293, 779],
        '个体自由': [624, 134, 104, 79, 124, 99, 62, 92, 122, 74, 222, 169, 270, 176, 99, 117, 396, 1555, 693, 172, 160,
                 233, 150, 79, 124, 128, 180, 166, 2576, 84, 54, 68, 122, 55, 264, 712],
        '祖国强大': [15, 10, 7, 6, 16, 7, 4, 7, 4, 2, 11, 11, 5, 9, 3, 12, 15, 18, 23, 9, 6, 8, 16, 8, 6, 3, 5, 9, 20, 4, 4,
                 3, 8, 5, 15, 36],
        '成为富人': [114, 27, 16, 22, 37, 20, 9, 24, 40, 16, 59, 69, 30, 38, 34, 31, 78, 64, 80, 50, 31, 55, 34, 28, 25, 23,
                 33, 47, 138, 22, 18, 17, 13, 19, 66, 82],
        '平等机会': [181, 43, 27, 21, 49, 45, 27, 34, 136, 30, 82, 66, 80, 53, 33, 41, 83, 62, 125, 61, 51, 67, 47, 33, 28,
                 34, 37, 62, 184, 30, 26, 35, 33, 29, 104, 163],
        '安享晚年': [101, 22, 16, 13, 37, 7, 5, 15, 30, 4, 61, 52, 35, 35, 14, 11, 117, 70, 73, 56, 41, 60, 33, 8, 25, 20,
                 39, 44, 158, 4, 2, 4, 14, 7, 51, 138],
        '收入足够': [41, 13, 7, 8, 12, 10, 4, 14, 15, 6, 26, 9, 14, 13, 15, 13, 21, 27, 29, 15, 19, 16, 8, 8, 12, 14, 11,
                 10, 64, 13, 9, 9, 10, 15, 21, 36],
        '中国经济持续发展': [8, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 12, 0, 1, 2, 3, 3, 0, 2, 1, 0, 2, 0, 1, 1, 0, 3, 0, 0, 0, 1,
                     0, 0, 3],
        '父辈更好': [8, 0, 0, 0, 1, 0, 0, 1, 2, 0, 3, 1, 0, 1, 1, 0, 3, 1, 3, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0,
                 2, 6]}, '201507': {
        '健康': [91268, 29310, 22345, 20821, 35889, 21881, 18922, 26927, 33676, 17995, 73163, 46294, 33688, 38740, 25851,
               28462, 66383, 64378, 61573, 41396, 34711, 47850, 33297, 22399, 25951, 29903, 33035, 43986, 132334, 20767,
               16910, 20980, 23736, 16940, 57464, 125921],
        '生活幸福': [15412, 6051, 5073, 4057, 7016, 5087, 3914, 5328, 6855, 4020, 13552, 8475, 6654, 7925, 5089, 5524,
                 10316, 9471, 9497, 8153, 6324, 7808, 5684, 5118, 4969, 5488, 6143, 7200, 23080, 4544, 3559, 3750, 3887,
                 3405, 7870, 17618],
        '有房': [2638, 605, 473, 396, 825, 429, 352, 510, 712, 410, 1562, 927, 912, 822, 538, 581, 1595, 1680, 1412, 940,
               763, 1036, 620, 422, 524, 684, 700, 1160, 4824, 391, 338, 379, 451, 399, 1397, 2283],
        '成为富人': [98, 33, 25, 26, 30, 22, 23, 30, 41, 16, 90, 38, 38, 41, 29, 31, 78, 73, 66, 45, 48, 37, 41, 28, 33, 24,
                 40, 33, 126, 18, 8, 27, 29, 32, 61, 69],
        '发展机会': [1053, 350, 328, 284, 426, 321, 311, 317, 407, 292, 937, 454, 356, 389, 345, 305, 606, 535, 767, 443,
                 400, 498, 370, 312, 338, 368, 395, 425, 1235, 311, 293, 283, 332, 268, 548, 1840],
        '出名': [3674, 1096, 780, 782, 1349, 780, 659, 926, 1124, 611, 2847, 1536, 1324, 1414, 909, 1104, 2847, 2509,
               2839, 1651, 1403, 2084, 1289, 841, 946, 1255, 1080, 1769, 4987, 744, 627, 761, 986, 652, 3335, 4653],
        '好工作': [1700, 481, 338, 304, 656, 284, 238, 405, 583, 257, 1336, 926, 645, 642, 397, 447, 1483, 1224, 1252, 810,
                1084, 924, 598, 323, 390, 595, 553, 813, 2510, 333, 198, 259, 333, 221, 1363, 2880],
        '家庭幸福': [2287, 931, 712, 654, 998, 703, 621, 769, 911, 606, 2067, 1457, 938, 1058, 772, 829, 1597, 1489, 1491,
                 1094, 1041, 1304, 820, 684, 788, 805, 1004, 1169, 3365, 643, 518, 602, 657, 512, 1477, 3272],
        '个体自由': [562, 101, 73, 61, 122, 64, 49, 66, 107, 49, 245, 132, 168, 111, 78, 82, 222, 277, 243, 140, 100, 150,
                 111, 80, 64, 89, 119, 135, 1697, 65, 56, 91, 95, 83, 288, 475],
        '平等机会': [141, 59, 42, 34, 61, 45, 29, 34, 36, 27, 110, 67, 48, 52, 21, 39, 91, 90, 85, 55, 46, 61, 51, 35, 35,
                 28, 32, 45, 156, 34, 25, 28, 28, 43, 95, 119],
        '个人努力': [161, 43, 41, 69, 51, 37, 34, 39, 68, 29, 122, 119, 58, 76, 48, 55, 122, 123, 123, 64, 57, 82, 120, 41,
                 54, 46, 52, 80, 268, 44, 36, 33, 33, 21, 101, 157],
        '事业有成': [420, 205, 141, 140, 251, 145, 173, 188, 208, 135, 440, 309, 203, 228, 153, 189, 312, 313, 311, 273,
                 203, 253, 186, 133, 142, 200, 217, 249, 697, 161, 130, 146, 158, 128, 286, 782],
        '白手起家': [283, 83, 55, 59, 110, 59, 53, 87, 101, 49, 203, 159, 118, 123, 69, 100, 199, 197, 210, 129, 98, 118,
                 89, 69, 73, 106, 81, 136, 415, 53, 33, 64, 49, 42, 216, 565],
        '祖国强大': [28, 4, 7, 8, 14, 6, 3, 4, 17, 5, 23, 19, 12, 11, 6, 9, 20, 12, 14, 8, 8, 10, 13, 3, 5, 4, 5, 13, 24, 5,
                 2, 2, 4, 2, 18, 38],
        '安享晚年': [81, 18, 8, 10, 14, 7, 10, 11, 27, 1, 44, 72, 27, 21, 22, 13, 60, 51, 63, 29, 39, 43, 21, 11, 17, 21,
                 23, 55, 95, 10, 6, 4, 6, 2, 49, 135],
        '收入足够': [36, 11, 6, 13, 12, 9, 8, 9, 23, 8, 29, 18, 29, 19, 12, 17, 33, 29, 33, 19, 15, 21, 15, 11, 21, 13, 10,
                 16, 45, 10, 5, 9, 11, 10, 24, 19],
        '中国经济持续发展': [3, 0, 0, 0, 3, 1, 0, 1, 0, 0, 2, 0, 2, 3, 0, 0, 3, 1, 6, 3, 1, 0, 1, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0,
                     0, 2, 13],
        '父辈更好': [2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                 2, 2]}, '201508': {
        '健康': [131221, 49174, 44594, 37750, 58033, 41857, 38253, 47794, 53422, 35951, 225583, 68218, 56957, 67498,
               47403, 48740, 95527, 89165, 87047, 59971, 56801, 76683, 56652, 39508, 44390, 50100, 54149, 65306, 192631,
               40069, 33630, 40535, 43014, 36217, 93305, 166928],
        '出名': [4933, 2015, 1461, 1523, 2145, 1418, 1344, 1649, 1974, 1282, 9027, 2545, 2225, 2496, 1679, 1804, 4322,
               3720, 4398, 2511, 2178, 3090, 2173, 1512, 1705, 2069, 1951, 2790, 7237, 1449, 1182, 1555, 1844, 1361,
               5583, 5939],
        '生活幸福': [24946, 9183, 8468, 7625, 11332, 8336, 7714, 10339, 9929, 7614, 50838, 13113, 10777, 14946, 8906, 9254,
                 17266, 15894, 16709, 11904, 10581, 12353, 10105, 7929, 8704, 9027, 10412, 11832, 38671, 8078, 6932,
                 7729, 7982, 7164, 14471, 20353],
        '家庭幸福': [3723, 1636, 1292, 1106, 1558, 1278, 1134, 1410, 1547, 1071, 6799, 2141, 1819, 1813, 1370, 1475, 2607,
                 2286, 2530, 1759, 1630, 1996, 1463, 1172, 1315, 1443, 1531, 1709, 5078, 1174, 964, 1202, 1226, 1064,
                 2492, 3407],
        '发展机会': [1636, 740, 656, 656, 800, 717, 688, 663, 765, 687, 4904, 873, 815, 792, 752, 661, 1107, 1003, 1395,
                 1014, 897, 858, 880, 648, 694, 776, 807, 819, 1894, 722, 591, 679, 746, 653, 1047, 1085],
        '有房': [3320, 990, 777, 764, 1274, 788, 718, 930, 1179, 766, 4757, 1480, 1392, 1326, 906, 984, 2061, 2318, 1938,
               1246, 1219, 1605, 1217, 776, 870, 1093, 1095, 1442, 6612, 798, 628, 779, 856, 731, 2391, 2674],
        '事业有成': [837, 340, 286, 300, 367, 292, 278, 346, 332, 287, 1835, 496, 365, 448, 349, 312, 624, 542, 557, 440,
                 369, 425, 353, 296, 338, 381, 380, 405, 1292, 313, 270, 322, 289, 282, 548, 743],
        '好工作': [2337, 663, 484, 513, 841, 471, 453, 565, 742, 434, 3201, 1061, 988, 857, 571, 642, 1800, 1341, 1497,
                1005, 1190, 1273, 656, 534, 590, 705, 696, 1013, 2578, 485, 436, 498, 512, 419, 1536, 2180],
        '安享晚年': [152, 44, 18, 19, 57, 18, 17, 25, 39, 16, 106, 65, 52, 43, 32, 36, 129, 93, 86, 57, 52, 121, 37, 23, 37,
                 46, 52, 93, 231, 25, 11, 16, 22, 14, 61, 216],
        '个人努力': [192, 76, 56, 64, 73, 64, 46, 63, 65, 55, 302, 87, 86, 83, 66, 68, 134, 110, 106, 101, 67, 81, 87, 51,
                 60, 75, 58, 112, 204, 54, 39, 69, 64, 58, 119, 180],
        '祖国强大': [120, 21, 15, 15, 22, 13, 9, 10, 18, 3, 68, 26, 31, 25, 13, 14, 56, 38, 59, 28, 37, 26, 7, 7, 37, 12,
                 18, 36, 74, 8, 8, 10, 10, 3, 45, 96],
        '个体自由': [1065, 132, 119, 137, 159, 115, 105, 132, 124, 104, 597, 194, 282, 190, 116, 153, 317, 297, 316, 214,
                 159, 220, 187, 98, 131, 145, 185, 212, 2139, 107, 111, 103, 127, 126, 371, 371],
        '白手起家': [617, 179, 162, 123, 260, 134, 118, 193, 215, 103, 898, 364, 254, 281, 166, 225, 492, 412, 418, 262,
                 231, 317, 194, 135, 186, 197, 183, 282, 1042, 139, 94, 122, 159, 126, 751, 706],
        '成为富人': [142, 51, 52, 42, 76, 46, 46, 57, 54, 58, 324, 120, 66, 91, 71, 66, 100, 117, 112, 65, 76, 88, 71, 43,
                 72, 65, 57, 74, 363, 51, 57, 49, 55, 50, 85, 103],
        '收入足够': [56, 24, 13, 20, 20, 17, 16, 23, 23, 25, 122, 29, 29, 28, 34, 20, 31, 39, 35, 33, 27, 26, 20, 19, 9, 28,
                 18, 25, 125, 20, 19, 12, 20, 19, 45, 33],
        '平等机会': [211, 80, 88, 77, 108, 84, 72, 97, 79, 77, 465, 104, 93, 109, 77, 94, 145, 124, 162, 109, 83, 165, 101,
                 67, 88, 95, 98, 122, 192, 80, 78, 58, 71, 86, 143, 215],
        '中国经济持续发展': [14, 2, 2, 0, 4, 0, 2, 0, 1, 0, 2, 3, 1, 245, 0, 1, 86, 1, 8, 0, 1, 1, 2, 0, 1, 1, 1, 1, 3, 0, 0, 0,
                     1, 0, 5, 15],
        '父辈更好': [3, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 2, 1, 2, 1, 1, 2, 0, 0, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0,
                 5, 3]}, '201509': {
        '家庭幸福': [3539, 1171, 1062, 955, 1491, 1064, 960, 1183, 1457, 858, 4798, 1882, 1459, 1649, 1246, 1264, 2540,
                 3000, 2652, 1597, 1525, 1995, 1352, 980, 1072, 1226, 1432, 1672, 6251, 976, 779, 877, 999, 796, 2082,
                 3807],
        '健康': [121211, 39034, 35961, 28570, 50434, 36504, 28981, 36726, 46737, 28347, 162934, 65702, 49701, 56091,
               38460, 40913, 90849, 86590, 80457, 52428, 49223, 61147, 48761, 30958, 36815, 43028, 45884, 59830, 195336,
               30605, 25275, 32481, 35400, 27688, 79806, 116049],
        '生活幸福': [25398, 7924, 7385, 6307, 10192, 6928, 6261, 7764, 9112, 6483, 36231, 12519, 9881, 12556, 7746, 8244,
                 17449, 14982, 14829, 11515, 9725, 12322, 9035, 6762, 7679, 8138, 8625, 10967, 41087, 6761, 5584, 6459,
                 7005, 5782, 12569, 23213],
        '出名': [3735, 1280, 1023, 934, 1552, 1059, 914, 1164, 1340, 980, 5657, 1743, 1633, 1790, 1243, 1368, 3243, 2607,
               2967, 1746, 1533, 2095, 1580, 1048, 1188, 1455, 1309, 1975, 5867, 1031, 819, 1083, 1181, 971, 3694,
               4507],
        '收入足够': [60, 28, 15, 8, 18, 15, 12, 9, 16, 10, 86, 29, 19, 16, 13, 14, 30, 32, 34, 24, 19, 23, 22, 17, 17, 18,
                 23, 49, 128, 11, 10, 10, 11, 7, 30, 45],
        '有房': [3646, 920, 678, 586, 1061, 594, 589, 742, 920, 671, 3363, 1278, 1103, 1192, 842, 747, 1813, 2233, 1780,
               1124, 1129, 1306, 977, 674, 746, 835, 954, 1185, 7973, 654, 462, 611, 710, 553, 2014, 2740],
        '发展机会': [1517, 581, 512, 472, 711, 551, 488, 508, 568, 484, 2695, 831, 652, 658, 493, 550, 870, 1080, 1165, 739,
                 619, 698, 594, 498, 518, 572, 588, 611, 1771, 514, 446, 548, 498, 485, 894, 994],
        '事业有成': [667, 310, 285, 247, 331, 228, 222, 256, 306, 239, 1243, 423, 330, 348, 242, 268, 480, 479, 512, 346,
                 315, 366, 334, 250, 304, 297, 310, 374, 1034, 269, 204, 225, 223, 207, 458, 747],
        '好工作': [1900, 594, 486, 367, 658, 397, 359, 523, 640, 337, 2282, 924, 687, 705, 534, 560, 1394, 1315, 1258, 940,
                1074, 921, 686, 398, 489, 711, 546, 851, 2460, 407, 314, 391, 393, 303, 1468, 2253],
        '平等机会': [212, 60, 60, 47, 66, 42, 56, 57, 67, 42, 289, 94, 68, 69, 60, 64, 129, 142, 130, 77, 59, 90, 56, 59,
                 48, 58, 86, 81, 240, 58, 49, 62, 60, 45, 168, 200],
        '白手起家': [738, 141, 128, 101, 222, 100, 76, 154, 178, 92, 604, 223, 178, 256, 133, 176, 338, 384, 326, 215, 183,
                 210, 152, 104, 135, 141, 153, 249, 815, 70, 96, 96, 107, 89, 326, 803],
        '祖国强大': [257, 50, 42, 41, 71, 30, 25, 36, 70, 21, 145, 117, 116, 72, 32, 47, 153, 140, 124, 68, 67, 95, 58, 34,
                 34, 47, 59, 80, 248, 30, 13, 13, 16, 5, 109, 339],
        '个人努力': [195, 53, 60, 51, 96, 52, 50, 62, 66, 48, 291, 98, 90, 86, 54, 67, 136, 129, 138, 101, 67, 107, 107, 55,
                 55, 64, 72, 89, 247, 57, 40, 65, 52, 46, 160, 267],
        '个体自由': [1176, 117, 94, 82, 126, 84, 63, 111, 131, 73, 436, 162, 216, 166, 123, 111, 254, 260, 324, 180, 143,
                 197, 197, 90, 91, 108, 159, 183, 4147, 83, 61, 85, 114, 114, 255, 454],
        '成为富人': [132, 40, 50, 35, 69, 40, 33, 43, 44, 23, 212, 84, 64, 57, 39, 37, 107, 75, 96, 65, 50, 74, 52, 36, 43,
                 49, 43, 56, 149, 36, 34, 30, 44, 43, 53, 87],
        '安享晚年': [129, 18, 14, 11, 40, 11, 3, 25, 32, 10, 82, 62, 51, 25, 31, 31, 126, 91, 99, 50, 54, 69, 34, 18, 24,
                 47, 32, 77, 178, 12, 4, 13, 13, 3, 73, 150],
        '中国经济持续发展': [14, 2, 0, 0, 1, 0, 0, 0, 1, 0, 1, 2, 4, 83, 0, 1, 42, 0, 11, 3, 1, 3, 5, 1, 0, 4, 0, 3, 4, 0, 0, 0,
                     0, 0, 0, 2],
        '父辈更好': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 3, 4, 0, 0, 0, 0, 0,
                 0, 4]}, '201510': {
        '生活幸福': [26774, 6829, 5850, 4996, 8865, 5639, 4677, 6263, 7967, 4748, 31188, 11367, 8240, 9587, 6473, 7001,
                 15630, 14075, 13126, 10010, 8474, 11395, 7394, 5369, 6215, 6529, 7768, 10473, 59572, 5214, 4367, 5179,
                 5616, 4550, 11826, 21999],
        '健康': [118204, 31478, 27054, 23468, 52220, 29472, 22286, 30144, 43305, 22516, 135167, 55993, 43416, 47743,
               35990, 38760, 85585, 78501, 75912, 46527, 42074, 60295, 47926, 25699, 29128, 35128, 43762, 59637, 197530,
               22670, 20354, 27031, 34948, 19298, 70941, 151894],
        '个体自由': [2811, 224, 103, 89, 116, 109, 73, 115, 107, 86, 421, 209, 170, 190, 139, 118, 305, 270, 353, 184, 163,
                 197, 243, 93, 119, 117, 156, 207, 10865, 88, 85, 73, 92, 71, 217, 580],
        '出名': [4066, 1155, 883, 750, 1382, 787, 693, 956, 1256, 721, 5330, 1693, 1471, 1530, 1045, 1129, 3219, 2627,
               3203, 1819, 1415, 2019, 1383, 868, 1075, 1172, 1225, 2058, 6528, 822, 622, 838, 1054, 722, 3704, 5050],
        '家庭幸福': [3582, 900, 743, 645, 2766, 748, 618, 846, 1287, 556, 3700, 1614, 1212, 1296, 937, 922, 2622, 2069,
                 2454, 1240, 2095, 1440, 1037, 677, 826, 917, 1235, 1568, 6453, 664, 530, 2596, 702, 565, 2022, 5081],
        '事业有成': [819, 202, 161, 170, 262, 143, 173, 172, 218, 174, 958, 317, 275, 276, 215, 221, 448, 404, 411, 239,
                 237, 276, 209, 195, 197, 208, 238, 315, 1253, 165, 141, 189, 163, 157, 347, 874],
        '好工作': [1596, 411, 323, 294, 663, 278, 201, 352, 567, 259, 1923, 730, 601, 623, 386, 395, 1174, 1141, 1098, 834,
                987, 784, 532, 298, 382, 467, 432, 725, 2460, 277, 221, 288, 344, 226, 1239, 2098],
        '有房': [6125, 871, 613, 533, 1063, 572, 510, 722, 973, 546, 3125, 1320, 991, 1246, 864, 805, 1957, 2218, 1968,
               1065, 1034, 1205, 836, 564, 662, 779, 896, 1232, 17778, 662, 474, 463, 518, 435, 1933, 3128],
        '发展机会': [1344, 318, 322, 255, 457, 327, 278, 342, 425, 291, 1939, 618, 411, 441, 358, 350, 710, 645, 991, 417,
                 432, 537, 430, 303, 347, 352, 408, 552, 1570, 314, 261, 323, 362, 304, 683, 1050],
        '白手起家': [865, 74, 77, 68, 120, 51, 50, 90, 108, 56, 400, 231, 99, 150, 82, 115, 214, 234, 186, 100, 128, 156,
                 115, 83, 92, 109, 91, 143, 596, 47, 38, 83, 73, 43, 193, 422],
        '个人努力': [205, 59, 54, 40, 93, 61, 55, 64, 66, 46, 264, 119, 82, 100, 81, 56, 134, 110, 119, 95, 65, 94, 60, 53,
                 76, 72, 52, 102, 221, 46, 41, 53, 52, 41, 122, 208],
        '祖国强大': [77, 18, 7, 8, 21, 15, 3, 13, 22, 3, 51, 32, 15, 29, 6, 19, 28, 30, 30, 24, 14, 20, 13, 4, 12, 13, 25,
                 14, 91, 4, 3, 6, 9, 3, 32, 68],
        '平等机会': [250, 46, 32, 28, 40, 31, 19, 37, 42, 24, 178, 65, 52, 50, 36, 39, 109, 95, 146, 57, 53, 85, 36, 33, 48,
                 45, 34, 71, 235, 23, 10, 16, 28, 18, 124, 237],
        '成为富人': [103, 35, 29, 28, 45, 35, 20, 25, 44, 25, 191, 48, 36, 57, 30, 31, 110, 77, 71, 52, 38, 46, 19, 24, 36,
                 45, 31, 63, 157, 24, 22, 30, 32, 27, 52, 124],
        '安享晚年': [142, 33, 11, 9, 30, 27, 5, 17, 28, 1, 81, 100, 91, 20, 10, 21, 117, 78, 58, 48, 83, 63, 24, 14, 27, 23,
                 34, 92, 177, 6, 2, 5, 14, 1, 55, 173],
        '父辈更好': [2, 0, 0, 0, 1, 0, 0, 0, 3, 0, 1, 3, 1, 1, 0, 0, 1, 2, 3, 4, 1, 1, 0, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0,
                 2, 2],
        '收入足够': [50, 5, 2, 2, 4, 4, 1, 7, 6, 1, 17, 8, 8, 13, 2, 4, 10, 16, 20, 10, 4, 13, 3, 3, 3, 7, 4, 10, 48, 4, 2,
                 2, 4, 8, 22, 46],
        '中国经济持续发展': [14, 0, 1, 1, 1, 1, 0, 1, 0, 0, 3, 2, 3, 3, 0, 1, 9, 4, 12, 3, 1, 4, 1, 0, 1, 1, 1, 3, 11, 0, 1, 0,
                     0, 0, 3, 12]}, '201511': {
        '健康': [134157, 31143, 29986, 23672, 49171, 29478, 21348, 30754, 47096, 20047, 100838, 65658, 44588, 56666,
               33157, 39507, 98658, 92424, 78961, 51639, 47658, 59581, 48624, 27144, 31626, 38371, 46293, 81732, 234260,
               23588, 19410, 22478, 25033, 15447, 74347, 159515],
        '个体自由': [878, 139, 103, 92, 151, 119, 105, 142, 153, 69, 392, 201, 219, 212, 153, 151, 434, 322, 394, 219, 198,
                 217, 156, 119, 128, 164, 169, 294, 13224, 116, 80, 85, 104, 104, 291, 899],
        '家庭幸福': [3122, 815, 913, 743, 1304, 857, 666, 846, 1379, 580, 2867, 2345, 1280, 1486, 979, 1066, 2550, 2138,
                 1963, 1620, 1350, 1530, 1007, 806, 967, 1091, 1176, 2369, 7280, 711, 518, 535, 618, 457, 1507, 4251],
        '生活幸福': [23783, 6498, 6765, 5481, 9678, 6376, 5717, 6827, 9322, 4866, 23475, 12989, 9459, 11316, 7507, 9434,
                 18543, 16647, 13928, 11117, 9702, 11968, 8845, 6149, 7175, 7574, 7830, 15741, 75880, 6075, 4591, 4821,
                 5184, 4153, 11203, 27104],
        '白手起家': [703, 84, 95, 59, 134, 71, 71, 111, 125, 47, 512, 231, 146, 171, 75, 137, 313, 273, 301, 187, 147, 217,
                 105, 89, 76, 112, 114, 270, 965, 65, 42, 51, 74, 46, 214, 669],
        '出名': [3797, 830, 761, 560, 1097, 630, 523, 726, 1097, 457, 3052, 2024, 1135, 1340, 896, 890, 2687, 2362, 2840,
               1433, 1409, 1783, 1084, 659, 838, 978, 925, 2003, 5903, 628, 436, 554, 727, 509, 3445, 4645],
        '发展机会': [1398, 231, 199, 185, 362, 175, 164, 232, 323, 168, 904, 524, 344, 384, 212, 224, 661, 567, 974, 412,
                 332, 431, 347, 198, 238, 266, 264, 558, 1612, 184, 140, 163, 197, 136, 496, 1128],
        '有房': [3480, 699, 706, 532, 1191, 605, 555, 662, 1034, 614, 2582, 1487, 1155, 1333, 758, 890, 2213, 2433, 1891,
               1223, 1140, 1315, 820, 639, 677, 894, 889, 1762, 24508, 616, 404, 445, 540, 370, 1662, 3884],
        '平等机会': [262, 28, 35, 18, 55, 15, 19, 34, 58, 22, 140, 83, 58, 94, 33, 64, 129, 111, 180, 65, 49, 94, 59, 25,
                 41, 32, 43, 84, 259, 20, 19, 23, 31, 17, 158, 231],
        '事业有成': [668, 241, 235, 163, 297, 190, 176, 211, 285, 147, 724, 383, 288, 352, 226, 228, 618, 467, 472, 311,
                 304, 326, 329, 193, 233, 287, 243, 472, 1366, 180, 145, 142, 150, 118, 359, 1051],
        '好工作': [1964, 444, 351, 293, 678, 286, 291, 371, 710, 177, 1388, 934, 676, 784, 422, 515, 1576, 1440, 1297, 908,
                1069, 941, 712, 393, 465, 552, 606, 1042, 2887, 301, 238, 310, 343, 237, 1302, 3417],
        '安享晚年': [98, 26, 7, 6, 22, 9, 12, 13, 24, 2, 74, 37, 27, 31, 9, 11, 55, 48, 42, 26, 21, 41, 25, 11, 9, 31, 12,
                 41, 97, 6, 1, 3, 6, 2, 29, 95],
        '个人努力': [202, 49, 53, 54, 95, 40, 42, 78, 63, 45, 175, 101, 74, 90, 62, 60, 159, 132, 117, 95, 75, 93, 56, 58,
                 62, 75, 52, 131, 323, 53, 41, 30, 44, 22, 130, 304],
        '成为富人': [136, 36, 23, 17, 47, 20, 25, 39, 39, 11, 99, 58, 31, 41, 19, 21, 80, 58, 47, 44, 36, 59, 26, 27, 29,
                 36, 28, 52, 168, 19, 18, 18, 20, 17, 55, 101],
        '收入足够': [33, 5, 6, 1, 5, 5, 1, 7, 5, 2, 14, 13, 11, 13, 3, 4, 27, 10, 21, 16, 10, 12, 6, 3, 0, 10, 5, 15, 61, 3,
                 2, 3, 4, 1, 24, 45],
        '祖国强大': [28, 11, 6, 6, 9, 6, 4, 6, 15, 0, 21, 20, 7, 19, 6, 6, 28, 22, 20, 23, 17, 9, 14, 4, 5, 7, 15, 19, 26,
                 3, 1, 2, 4, 1, 20, 33],
        '中国经济持续发展': [6, 1, 0, 5, 2, 0, 0, 0, 0, 0, 3, 5, 0, 4, 0, 0, 3, 5, 3, 1, 1, 2, 0, 0, 2, 0, 4, 1, 5, 0, 0, 0, 1,
                     0, 4, 3],
        '父辈更好': [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 4, 2, 0, 1, 0, 0, 1, 0, 1, 2, 4, 0, 0, 0, 0, 0,
                 1, 3]}, '201512': {
        '健康': [145936, 30781, 27318, 18959, 52014, 26410, 18431, 31200, 46762, 14850, 92130, 78299, 43771, 53584, 33141,
               38262, 101223, 95272, 89323, 50406, 48130, 59791, 37636, 21403, 27429, 36914, 42001, 80187, 233915,
               19348, 14685, 15584, 22189, 10295, 69196, 201934],
        '家庭幸福': [4164, 918, 890, 747, 1595, 876, 672, 1029, 1456, 605, 2820, 2265, 1375, 1826, 1032, 1194, 3027, 2783,
                 2379, 1604, 1498, 1917, 1059, 814, 970, 1109, 1356, 2556, 7361, 704, 535, 456, 627, 373, 1775, 6201],
        '生活幸福': [26619, 6930, 6539, 5123, 10822, 6103, 5252, 7244, 9314, 4520, 21021, 14764, 9564, 11765, 7410, 7988,
                 19239, 19040, 15584, 11005, 10029, 11697, 7615, 6014, 7097, 7643, 9135, 16967, 53442, 5790, 4238, 4107,
                 4918, 3323, 10689, 37318],
        '有房': [3934, 834, 654, 540, 1341, 643, 549, 776, 1047, 637, 2328, 1835, 1384, 1420, 842, 868, 2366, 2954, 2157,
               1320, 1185, 1442, 932, 641, 736, 929, 1055, 1948, 10427, 634, 381, 365, 457, 321, 1901, 4624],
        '出名': [4097, 763, 578, 513, 1075, 516, 412, 695, 1053, 356, 2256, 1779, 1014, 1334, 730, 869, 2533, 2345, 2666,
               1358, 1099, 1727, 1064, 618, 751, 809, 870, 2024, 6026, 539, 286, 435, 611, 306, 3296, 5286],
        '好工作': [1999, 463, 340, 221, 721, 286, 189, 409, 666, 173, 1365, 1056, 615, 801, 402, 403, 1562, 1397, 1287,
                863, 1054, 1084, 588, 282, 377, 515, 509, 974, 2877, 243, 148, 181, 207, 113, 1350, 3005],
        '发展机会': [1459, 193, 162, 160, 353, 189, 133, 212, 308, 107, 707, 556, 304, 348, 210, 263, 615, 693, 1013, 370,
                 313, 407, 215, 158, 217, 255, 247, 768, 1855, 148, 112, 80, 126, 57, 472, 1161],
        '平等机会': [278, 44, 30, 18, 81, 30, 15, 35, 74, 18, 135, 137, 45, 55, 38, 44, 125, 113, 141, 66, 60, 98, 53, 26,
                 34, 37, 47, 106, 287, 21, 18, 12, 20, 14, 146, 311],
        '父辈更好': [7, 2, 3, 1, 0, 0, 1, 1, 4, 0, 4, 4, 2, 1, 2, 3, 11, 1, 1, 1, 3, 2, 0, 2, 3, 1, 1, 0, 8, 2, 2, 1, 1, 2,
                 4, 7],
        '安享晚年': [139, 19, 14, 11, 43, 13, 4, 23, 37, 10, 108, 161, 45, 34, 7, 21, 105, 78, 73, 45, 71, 48, 38, 27, 21,
                 51, 36, 74, 584, 9, 5, 3, 25, 3, 89, 190],
        '事业有成': [818, 232, 199, 130, 342, 182, 154, 234, 301, 136, 628, 466, 277, 326, 238, 232, 633, 539, 494, 334,
                 302, 396, 248, 192, 228, 245, 271, 574, 2332, 167, 121, 90, 144, 84, 359, 1359],
        '个人努力': [263, 41, 46, 42, 77, 27, 28, 50, 62, 36, 135, 87, 66, 90, 50, 49, 147, 115, 103, 72, 60, 79, 42, 35,
                 47, 46, 60, 132, 309, 35, 18, 21, 34, 24, 92, 264],
        '祖国强大': [29, 11, 3, 9, 12, 6, 4, 6, 12, 4, 34, 27, 17, 13, 8, 8, 27, 18, 27, 7, 8, 11, 12, 6, 5, 8, 19, 26, 57,
                 10, 2, 5, 11, 1, 37, 57],
        '个体自由': [814, 220, 126, 81, 167, 111, 85, 118, 149, 71, 329, 214, 231, 190, 173, 134, 346, 299, 420, 206, 159,
                 268, 169, 90, 114, 139, 180, 247, 4227, 110, 61, 66, 78, 95, 250, 817],
        '白手起家': [409, 86, 85, 77, 144, 73, 54, 102, 138, 38, 394, 218, 126, 150, 97, 178, 296, 277, 241, 175, 142, 176,
                 113, 68, 83, 87, 122, 257, 760, 72, 44, 45, 69, 29, 181, 583],
        '收入足够': [78, 6, 3, 4, 23, 4, 3, 10, 23, 0, 29, 21, 16, 17, 5, 9, 42, 33, 45, 25, 20, 31, 8, 8, 13, 9, 13, 17,
                 116, 8, 0, 3, 9, 3, 41, 59],
        '成为富人': [127, 30, 23, 19, 28, 24, 22, 36, 36, 13, 94, 60, 29, 48, 19, 31, 77, 96, 127, 39, 45, 48, 31, 21, 19,
                 45, 34, 52, 178, 13, 7, 15, 21, 10, 66, 125],
        '中国经济持续发展': [15, 0, 0, 0, 4, 1, 0, 1, 2, 1, 10, 4, 2, 4, 0, 0, 3, 2, 10, 0, 2, 1, 0, 0, 0, 1, 0, 2, 12, 1, 0, 0,
                     1, 0, 1, 3]}, '201601': {
        '健康': [146690, 32182, 23953, 18207, 52624, 22502, 15491, 29060, 46615, 13200, 84352, 67821, 42397, 53387, 30389,
               35884, 102674, 101288, 102978, 52519, 46976, 61614, 36907, 20204, 26061, 35579, 37504, 77625, 272006,
               17052, 11437, 15428, 20254, 7594, 82744, 257653],
        '事业有成': [1332, 261, 185, 170, 503, 160, 102, 230, 339, 103, 568, 493, 333, 370, 225, 268, 774, 646, 723, 501,
                 330, 484, 250, 158, 192, 235, 248, 541, 2124, 166, 72, 71, 98, 63, 352, 2053],
        '生活幸福': [31769, 6702, 6117, 4483, 13181, 5754, 4105, 6752, 9612, 3854, 18199, 14186, 9346, 14471, 6947, 8200,
                 20071, 19654, 16547, 10725, 9628, 12164, 7878, 5200, 6307, 7770, 7859, 15949, 59537, 4458, 2955, 2516,
                 3466, 1997, 9676, 54876],
        '好工作': [2200, 471, 327, 263, 754, 569, 193, 453, 732, 136, 1271, 1011, 731, 818, 404, 545, 1636, 1472, 1490,
                903, 1149, 1064, 627, 274, 385, 556, 567, 1019, 3387, 227, 123, 214, 287, 130, 1453, 3876],
        '家庭幸福': [4662, 932, 895, 644, 2173, 997, 543, 926, 1542, 455, 2677, 2973, 1654, 1785, 1059, 1212, 3145, 2902,
                 2658, 1518, 1509, 2064, 1094, 676, 974, 1170, 1126, 2454, 8392, 599, 362, 351, 491, 253, 1855, 8698],
        '有房': [3697, 675, 531, 423, 1507, 551, 386, 707, 951, 581, 1887, 1438, 1062, 1376, 694, 786, 2326, 2867, 2165,
               1119, 989, 1375, 848, 508, 679, 953, 946, 1706, 12306, 476, 250, 289, 417, 242, 2399, 6509],
        '出名': [4303, 813, 542, 493, 1262, 444, 357, 787, 1021, 302, 2132, 1611, 1132, 1363, 758, 880, 2850, 2695, 3043,
               1466, 1159, 1835, 1138, 554, 660, 913, 951, 1987, 6409, 481, 219, 315, 540, 211, 3541, 7545],
        '安享晚年': [115, 10, 10, 16, 26, 12, 8, 10, 36, 1, 48, 53, 27, 28, 14, 17, 64, 59, 59, 31, 39, 39, 16, 10, 9, 24,
                 19, 44, 155, 6, 6, 5, 8, 3, 42, 126],
        '发展机会': [1435, 207, 229, 211, 384, 208, 189, 260, 395, 182, 738, 679, 321, 386, 235, 293, 794, 792, 892, 425,
                 380, 491, 299, 232, 275, 302, 294, 1199, 2083, 190, 161, 83, 111, 56, 535, 1565],
        '个体自由': [718, 155, 81, 89, 225, 91, 77, 120, 149, 49, 359, 283, 234, 237, 154, 146, 438, 473, 450, 228, 182,
                 242, 190, 113, 87, 183, 169, 242, 4950, 80, 44, 40, 116, 61, 227, 1349],
        '个人努力': [363, 46, 36, 30, 78, 32, 23, 40, 90, 25, 170, 136, 84, 89, 39, 50, 179, 183, 164, 97, 85, 108, 104, 24,
                 55, 45, 56, 139, 463, 34, 34, 14, 34, 15, 130, 494],
        '白手起家': [373, 83, 71, 57, 167, 57, 40, 96, 113, 40, 263, 196, 123, 167, 73, 117, 261, 263, 260, 149, 103, 182,
                 84, 63, 84, 107, 127, 212, 707, 49, 30, 31, 69, 18, 218, 662],
        '平等机会': [279, 32, 41, 20, 59, 23, 12, 33, 60, 12, 122, 98, 35, 52, 25, 44, 136, 130, 134, 83, 53, 63, 34, 15,
                 49, 32, 43, 79, 217, 22, 10, 8, 15, 6, 108, 255],
        '祖国强大': [66, 14, 9, 7, 14, 7, 3, 7, 19, 4, 45, 26, 14, 16, 16, 14, 54, 41, 34, 29, 16, 40, 16, 2, 6, 11, 15, 46,
                 73, 6, 5, 1, 9, 3, 54, 125],
        '成为富人': [142, 35, 26, 16, 67, 24, 12, 29, 53, 5, 98, 86, 36, 55, 20, 41, 102, 115, 96, 49, 33, 70, 45, 17, 29,
                 44, 33, 76, 290, 15, 7, 23, 13, 9, 85, 177],
        '收入足够': [60, 5, 5, 5, 13, 2, 3, 6, 14, 2, 23, 12, 4, 10, 5, 7, 32, 37, 37, 10, 9, 12, 16, 6, 8, 4, 7, 15, 254,
                 5, 1, 1, 19, 2, 37, 52],
        '中国经济持续发展': [11, 0, 0, 0, 1, 0, 1, 1, 2, 0, 2, 1, 1, 1, 0, 0, 3, 3, 9, 1, 3, 0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0,
                     0, 1, 9],
        '父辈更好': [6, 1, 3, 0, 2, 3, 1, 2, 1, 0, 6, 2, 0, 0, 2, 0, 6, 1, 3, 4, 0, 3, 2, 1, 3, 2, 1, 3, 1, 0, 0, 0, 1, 0,
                 4, 14]}, '201602': {
        '健康': [145388, 33152, 22236, 18150, 49616, 20754, 14237, 29579, 43070, 12328, 89147, 67145, 40485, 53987, 28995,
               35261, 107343, 99193, 98109, 52619, 49799, 64038, 38353, 20641, 26362, 33985, 35371, 67631, 279926,
               17836, 9134, 16998, 29808, 9077, 83675, 230779],
        '生活幸福': [28849, 7060, 5933, 4201, 11314, 5540, 4083, 6662, 8499, 3828, 17042, 13202, 9011, 14748, 6832, 7525,
                 19465, 19750, 16371, 9925, 9592, 11021, 8345, 4960, 5922, 7389, 7528, 13043, 54434, 4502, 2951, 3034,
                 5388, 2180, 9988, 45259],
        '出名': [3761, 850, 865, 362, 1029, 404, 311, 597, 809, 334, 1734, 1364, 1081, 1210, 698, 849, 2269, 2241, 2602,
               1238, 1086, 1512, 938, 498, 540, 906, 857, 2048, 7213, 400, 236, 371, 683, 230, 3030, 6487],
        '家庭幸福': [4922, 1153, 859, 777, 1787, 791, 563, 985, 1412, 488, 2840, 2393, 1431, 1881, 1213, 1192, 3511, 2987,
                 2963, 1845, 1698, 1966, 1265, 764, 950, 1288, 1440, 2394, 11222, 591, 338, 478, 945, 347, 2363, 8065],
        '好工作': [2227, 472, 303, 228, 763, 265, 146, 415, 713, 151, 1267, 988, 630, 752, 383, 406, 1662, 2337, 1451, 988,
                1335, 1036, 736, 279, 360, 490, 501, 1031, 3502, 221, 97, 155, 364, 109, 1531, 3396],
        '个体自由': [601, 126, 99, 81, 202, 78, 80, 112, 146, 55, 343, 253, 219, 222, 117, 158, 391, 739, 562, 203, 195,
                 232, 224, 75, 82, 160, 138, 281, 4612, 68, 39, 57, 121, 50, 259, 1142],
        '事业有成': [1424, 367, 270, 180, 614, 231, 167, 313, 514, 113, 892, 673, 386, 651, 311, 387, 1120, 1002, 962, 568,
                 478, 594, 337, 219, 271, 448, 418, 674, 2800, 183, 89, 121, 266, 87, 720, 2378],
        '个人努力': [258, 66, 42, 32, 99, 38, 25, 53, 70, 26, 133, 119, 73, 90, 53, 68, 161, 166, 113, 75, 78, 106, 63, 46,
                 37, 116, 40, 123, 424, 32, 26, 22, 33, 11, 125, 352],
        '有房': [3600, 753, 595, 426, 1215, 492, 336, 670, 952, 596, 1958, 1723, 1128, 1327, 708, 814, 2369, 3734, 2563,
               1142, 1132, 1350, 895, 506, 669, 825, 871, 1596, 11735, 470, 253, 352, 584, 233, 2136, 5709],
        '发展机会': [1164, 211, 126, 109, 306, 116, 86, 195, 261, 63, 640, 516, 241, 280, 145, 172, 549, 518, 755, 335, 324,
                 409, 238, 113, 123, 184, 186, 465, 1946, 103, 49, 89, 176, 67, 438, 1136],
        '白手起家': [407, 84, 57, 43, 132, 43, 34, 108, 105, 46, 225, 195, 116, 162, 100, 83, 255, 272, 259, 163, 135, 174,
                 90, 53, 59, 89, 87, 207, 701, 48, 28, 43, 71, 20, 238, 694],
        '中国经济持续发展': [13, 4, 0, 0, 0, 1, 0, 0, 0, 0, 1, 5, 1, 4, 0, 1, 1, 9, 5, 4, 10, 2, 1, 1, 0, 0, 1, 11, 11, 2, 0, 0,
                     1, 0, 7, 3],
        '收入足够': [52, 5, 9, 5, 23, 8, 5, 14, 26, 3, 37, 36, 20, 27, 9, 11, 42, 83, 38, 17, 12, 36, 13, 5, 10, 16, 19, 36,
                 490, 12, 0, 2, 22, 4, 39, 103],
        '平等机会': [161, 40, 21, 23, 45, 18, 13, 70, 32, 14, 73, 76, 32, 63, 24, 40, 86, 78, 105, 71, 52, 85, 34, 15, 24,
                 31, 31, 45, 230, 25, 7, 10, 13, 17, 98, 224],
        '成为富人': [119, 26, 17, 12, 47, 13, 12, 37, 43, 8, 97, 75, 37, 43, 25, 30, 125, 82, 86, 46, 35, 66, 40, 14, 29,
                 33, 34, 92, 280, 10, 13, 17, 30, 4, 115, 205],
        '安享晚年': [120, 26, 8, 14, 33, 5, 3, 16, 39, 5, 87, 45, 29, 37, 17, 15, 82, 77, 78, 51, 41, 80, 19, 18, 26, 32,
                 24, 50, 187, 12, 2, 6, 7, 5, 74, 160],
        '祖国强大': [23, 1, 9, 4, 10, 5, 0, 5, 9, 2, 15, 11, 8, 14, 8, 9, 13, 21, 13, 7, 5, 13, 6, 1, 10, 6, 8, 5, 11, 5, 1,
                 1, 0, 2, 18, 32],
        '父辈更好': [5, 2, 2, 2, 2, 1, 0, 0, 1, 3, 6, 2, 2, 4, 0, 2, 0, 10, 4, 2, 3, 2, 0, 0, 1, 1, 3, 1, 4, 1, 0, 1, 3, 2,
                 3, 9]}, '201603': {
        '健康': [89249, 18149, 13242, 10612, 29677, 13005, 8512, 16918, 27076, 7782, 52229, 40370, 28029, 32433, 17054,
               19664, 59715, 53523, 58034, 32731, 27941, 38073, 21798, 11924, 15296, 20311, 22515, 45248, 138314, 9805,
               5444, 8128, 13525, 4666, 44152, 126280],
        '事业有成': [516, 121, 89, 64, 145, 104, 62, 105, 137, 72, 271, 255, 175, 190, 114, 118, 649, 301, 277, 207, 172,
                 223, 130, 89, 108, 434, 139, 305, 792, 90, 45, 55, 78, 34, 218, 956],
        '安享晚年': [53, 11, 19, 1, 18, 8, 4, 13, 9, 2, 40, 23, 22, 20, 9, 14, 47, 40, 34, 26, 27, 30, 14, 8, 9, 24, 17, 20,
                 96, 4, 2, 2, 5, 2, 37, 86],
        '生活幸福': [19411, 4190, 3894, 3072, 7136, 3812, 3037, 4456, 6211, 2764, 11963, 8940, 6385, 11032, 4826, 5343,
                 12538, 11771, 10269, 6983, 6635, 7600, 5469, 3234, 4088, 4973, 5884, 11333, 31995, 3100, 2120, 1646,
                 2782, 1117, 7404, 32384],
        '出名': [2644, 456, 330, 251, 730, 308, 184, 368, 593, 202, 1275, 947, 690, 877, 424, 504, 1779, 1543, 1892, 953,
               766, 1110, 728, 315, 385, 575, 510, 1399, 3940, 258, 177, 225, 368, 137, 2226, 3733],
        '有房': [2818, 421, 364, 224, 840, 339, 231, 469, 632, 500, 1310, 993, 915, 883, 433, 511, 1640, 2376, 1902, 822,
               694, 875, 616, 290, 387, 622, 573, 1198, 6104, 286, 127, 186, 441, 129, 1401, 3800],
        '好工作': [1631, 317, 176, 168, 522, 178, 83, 254, 489, 80, 887, 753, 443, 538, 291, 305, 1222, 1400, 1062, 746,
                1012, 695, 581, 212, 283, 354, 396, 723, 2584, 183, 67, 125, 169, 56, 1176, 2817],
        '家庭幸福': [2893, 588, 526, 402, 987, 504, 347, 670, 776, 302, 1624, 1151, 768, 880, 598, 713, 1787, 1564, 1485,
                 1230, 855, 1137, 603, 404, 551, 661, 703, 1393, 4177, 308, 210, 214, 410, 134, 1030, 4413],
        '平等机会': [226, 46, 19, 18, 47, 12, 11, 37, 33, 8, 95, 62, 41, 54, 24, 26, 126, 105, 112, 46, 44, 77, 31, 19, 27,
                 49, 30, 37, 221, 9, 5, 7, 14, 10, 116, 207],
        '个体自由': [325, 52, 54, 50, 92, 43, 46, 60, 90, 39, 174, 205, 187, 107, 91, 85, 213, 333, 227, 110, 131, 108, 163,
                 62, 50, 80, 98, 198, 2159, 53, 27, 29, 121, 31, 164, 562],
        '发展机会': [964, 130, 108, 71, 223, 94, 84, 168, 189, 46, 430, 382, 219, 257, 136, 117, 406, 459, 744, 238, 396,
                 244, 163, 92, 127, 188, 150, 389, 1231, 73, 50, 61, 83, 31, 378, 826],
        '白手起家': [353, 53, 56, 44, 105, 40, 21, 61, 77, 23, 181, 120, 91, 109, 42, 60, 192, 214, 192, 109, 95, 124, 63,
                 39, 51, 68, 59, 195, 522, 31, 18, 31, 47, 18, 160, 483],
        '成为富人': [89, 12, 9, 10, 33, 10, 9, 20, 35, 2, 53, 37, 36, 33, 9, 23, 55, 44, 45, 28, 32, 31, 22, 14, 21, 16, 14,
                 44, 132, 5, 5, 12, 7, 4, 38, 115],
        '个人努力': [197, 42, 39, 13, 78, 27, 21, 35, 71, 24, 146, 104, 64, 84, 35, 55, 126, 116, 76, 67, 59, 79, 52, 30,
                 40, 112, 48, 100, 267, 60, 7, 19, 24, 8, 84, 262],
        '收入足够': [56, 5, 4, 3, 281, 4, 3, 11, 8, 4, 24, 28, 10, 18, 2, 5, 42, 26, 72, 17, 17, 17, 5, 5, 2, 6, 4, 155, 73,
                 6, 4, 5, 1, 5, 27, 266],
        '祖国强大': [35, 1, 5, 0, 7, 4, 0, 5, 15, 1, 11, 7, 5, 12, 7, 4, 14, 13, 19, 7, 3, 4, 3, 0, 1, 5, 4, 6, 18, 1, 2, 2,
                 4, 0, 10, 29],
        '父辈更好': [1, 0, 1, 2, 0, 1, 0, 0, 0, 0, 1, 2, 0, 1, 2, 0, 2, 1, 1, 2, 1, 2, 0, 0, 0, 1, 0, 0, 5, 0, 0, 0, 1, 0,
                 0, 7],
        '中国经济持续发展': [11, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0, 2, 0, 3, 0, 3, 1, 0, 1, 4, 1, 0, 0, 0, 1, 0, 5, 1, 0, 0, 0,
                     0, 2, 6]}, '201604': {
        '健康': [95050, 18526, 15809, 11788, 32285, 15003, 10477, 19874, 29044, 10571, 51027, 46204, 34829, 35097, 20148,
               23035, 67643, 62999, 65254, 35150, 32639, 43150, 25972, 13662, 18794, 25001, 29695, 59789, 155530, 11700,
               7576, 11500, 16658, 4554, 49550, 131119],
        '生活幸福': [17792, 4682, 4618, 3793, 7364, 4404, 3501, 5257, 6237, 3354, 9811, 9350, 6850, 11402, 5220, 5528,
                 11478, 11089, 11359, 6914, 6844, 7552, 5806, 4279, 4768, 5222, 6997, 11498, 24649, 3645, 2951, 1785,
                 2643, 817, 6946, 21670],
        '家庭幸福': [2504, 606, 528, 377, 919, 484, 343, 589, 777, 333, 1241, 1527, 917, 974, 591, 709, 1989, 1500, 1668,
                 913, 920, 1153, 749, 449, 568, 672, 953, 1616, 4075, 395, 269, 263, 287, 101, 1089, 3618],
        '好工作': [1876, 375, 228, 175, 702, 303, 245, 474, 514, 107, 876, 1183, 733, 777, 300, 378, 1404, 1355, 1213, 891,
                1035, 875, 407, 262, 286, 414, 1059, 933, 2919, 208, 88, 355, 375, 69, 1556, 2977],
        '白手起家': [344, 78, 63, 47, 174, 47, 31, 63, 98, 31, 161, 141, 104, 142, 83, 83, 238, 246, 340, 130, 125, 153, 73,
                 51, 58, 98, 68, 150, 560, 43, 14, 29, 33, 11, 140, 533],
        '出名': [3321, 547, 403, 325, 958, 410, 298, 485, 822, 310, 1568, 1231, 964, 973, 608, 697, 2294, 1987, 2240,
               1167, 1029, 1337, 794, 460, 579, 721, 791, 1786, 4788, 376, 173, 387, 446, 190, 2451, 4708],
        '事业有成': [439, 114, 81, 101, 149, 71, 59, 96, 126, 56, 290, 274, 181, 144, 89, 136, 278, 237, 262, 169, 183, 204,
                 87, 78, 84, 99, 114, 282, 599, 60, 46, 28, 63, 16, 222, 626],
        '有房': [2604, 440, 352, 252, 852, 366, 253, 455, 663, 416, 1190, 1024, 961, 845, 436, 457, 1570, 2219, 1595, 778,
               825, 796, 588, 332, 417, 627, 599, 1288, 3945, 273, 148, 239, 247, 128, 1270, 3237],
        '祖国强大': [39, 7, 7, 2, 12, 5, 5, 8, 15, 5, 15, 15, 13, 10, 10, 7, 22, 13, 13, 10, 8, 11, 6, 6, 10, 13, 5, 11, 18,
                 7, 1, 3, 1, 0, 22, 51],
        '发展机会': [1378, 137, 159, 176, 319, 144, 102, 173, 202, 92, 445, 853, 287, 264, 146, 199, 525, 625, 825, 293,
                 361, 314, 148, 210, 149, 226, 215, 609, 1306, 116, 80, 111, 122, 36, 387, 1062],
        '安享晚年': [99, 24, 16, 12, 31, 14, 12, 19, 32, 12, 58, 60, 46, 27, 18, 24, 71, 76, 74, 69, 45, 44, 19, 22, 21, 28,
                 42, 65, 177, 11, 8, 3, 9, 6, 53, 171],
        '个体自由': [335, 76, 47, 66, 112, 56, 35, 53, 86, 49, 147, 118, 192, 90, 78, 70, 229, 271, 221, 109, 175, 139, 162,
                 60, 66, 67, 121, 260, 962, 68, 29, 44, 48, 28, 186, 697],
        '成为富人': [104, 14, 16, 8, 40, 16, 11, 21, 54, 9, 49, 32, 31, 21, 20, 23, 65, 57, 53, 26, 29, 37, 21, 19, 13, 16,
                 23, 28, 133, 5, 10, 12, 11, 4, 70, 98],
        '个人努力': [236, 34, 31, 15, 84, 31, 26, 38, 64, 30, 85, 97, 47, 57, 43, 43, 179, 170, 91, 74, 57, 94, 55, 30, 92,
                 104, 69, 90, 298, 32, 21, 15, 16, 4, 81, 295],
        '平等机会': [165, 29, 14, 26, 32, 16, 7, 20, 50, 13, 53, 36, 38, 28, 20, 24, 70, 64, 88, 50, 47, 50, 24, 22, 23, 28,
                 21, 38, 115, 13, 5, 3, 11, 1, 114, 166],
        '父辈更好': [4, 0, 0, 0, 2, 0, 0, 2, 1, 0, 0, 0, 0, 1, 0, 1, 1, 2, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0,
                 4, 4],
        '收入足够': [40, 5, 5, 0, 13, 2, 4, 7, 5, 2, 18, 8, 10, 11, 2, 8, 35, 31, 33, 16, 11, 20, 6, 12, 3, 15, 9, 17, 53,
                 3, 1, 1, 3, 4, 20, 54],
        '中国经济持续发展': [13, 1, 2, 0, 1, 2, 1, 1, 4, 0, 8, 5, 1, 1, 0, 2, 10, 10, 9, 5, 1, 1, 1, 0, 0, 1, 2, 1, 13, 0, 2, 0,
                     0, 0, 5, 16]}, '201605': {
        '健康': [113514, 22120, 18148, 14006, 37064, 17555, 11589, 22651, 33295, 9975, 65749, 56972, 35363, 44239, 22061,
               26857, 88102, 69661, 74995, 43461, 40532, 50249, 26129, 16167, 21880, 27310, 30436, 59592, 173152, 14292,
               8119, 14805, 13249, 5645, 54432, 148822],
        '好工作': [1827, 367, 265, 234, 582, 259, 155, 458, 617, 150, 1077, 772, 1094, 805, 412, 396, 1290, 1341, 1033,
                821, 1304, 869, 427, 290, 293, 439, 559, 933, 2358, 186, 111, 340, 239, 88, 1197, 3167],
        '生活幸福': [19514, 3908, 3552, 2939, 6875, 3481, 2517, 4051, 5606, 2362, 11514, 8573, 6223, 9900, 4457, 4981,
                 13304, 10931, 12206, 6903, 6313, 7706, 5437, 3110, 4226, 4406, 4852, 9880, 24189, 2749, 2053, 4659,
                 2521, 1388, 7854, 24810],
        '家庭幸福': [3061, 633, 619, 392, 1151, 587, 317, 781, 1098, 299, 1900, 1514, 1003, 1029, 731, 779, 3502, 1768,
                 1786, 1188, 1014, 2456, 765, 472, 605, 850, 848, 1560, 6052, 421, 272, 468, 286, 133, 1394, 4089],
        '出名': [3776, 595, 492, 380, 1004, 455, 305, 593, 859, 301, 1926, 1352, 1040, 1102, 645, 743, 2819, 2105, 2359,
               1254, 1011, 1476, 819, 503, 625, 864, 783, 1950, 5070, 425, 238, 436, 446, 220, 2800, 5307],
        '有房': [2395, 442, 357, 284, 974, 341, 224, 545, 710, 446, 1476, 1028, 1043, 866, 440, 515, 1803, 2408, 1575,
               847, 754, 958, 789, 270, 468, 610, 642, 1213, 3428, 294, 178, 447, 297, 149, 1403, 3077],
        '发展机会': [1162, 193, 121, 158, 278, 138, 84, 168, 228, 76, 569, 377, 327, 237, 286, 188, 738, 526, 718, 327, 265,
                 340, 162, 152, 151, 231, 252, 490, 1431, 89, 57, 119, 106, 31, 364, 1274],
        '成为富人': [71, 14, 16, 15, 24, 20, 8, 18, 21, 3, 54, 35, 18, 30, 16, 17, 59, 41, 60, 30, 24, 22, 25, 18, 16, 24,
                 17, 25, 118, 12, 11, 12, 11, 13, 27, 92],
        '事业有成': [539, 99, 96, 120, 188, 103, 66, 112, 134, 43, 321, 287, 145, 184, 97, 132, 386, 306, 316, 187, 141,
                 220, 130, 82, 110, 104, 114, 238, 693, 66, 44, 84, 61, 27, 260, 699],
        '个体自由': [373, 64, 51, 45, 116, 71, 44, 66, 95, 37, 184, 113, 258, 110, 98, 77, 259, 177, 217, 117, 127, 129,
                 276, 48, 47, 91, 152, 225, 641, 49, 36, 64, 55, 59, 203, 575],
        '白手起家': [412, 56, 48, 43, 120, 33, 29, 67, 111, 27, 225, 166, 119, 115, 54, 90, 276, 264, 235, 136, 98, 155, 74,
                 50, 69, 107, 60, 141, 531, 35, 15, 42, 35, 13, 179, 493],
        '安享晚年': [119, 30, 41, 24, 41, 29, 22, 32, 47, 21, 81, 64, 89, 36, 43, 40, 122, 86, 107, 57, 66, 72, 26, 26, 41,
                 62, 77, 99, 272, 24, 18, 18, 19, 15, 59, 209],
        '个人努力': [1600, 716, 1000, 1981, 819, 2790, 1106, 1474, 1583, 1768, 1157, 3966, 5598, 2537, 712, 2874, 4896,
                 9884, 3015, 1059, 2315, 1301, 743, 2028, 1175, 2366, 4760, 4762, 3732, 2253, 1250, 3976, 2160, 294,
                 1781, 7610],
        '平等机会': [219, 25, 21, 12, 56, 20, 7, 28, 47, 3, 100, 70, 52, 41, 26, 22, 202, 80, 107, 75, 43, 68, 33, 17, 29,
                 26, 32, 64, 208, 13, 4, 16, 13, 4, 105, 233],
        '收入足够': [49, 9, 5, 1, 8, 3, 2, 4, 9, 2, 24, 10, 15, 13, 4, 12, 31, 25, 50, 20, 21, 21, 5, 4, 11, 8, 9, 11, 56,
                 4, 2, 3, 6, 0, 32, 60],
        '祖国强大': [46, 7, 5, 1, 9, 8, 7, 6, 6, 7, 17, 12, 11, 14, 9, 10, 26, 9, 14, 12, 12, 14, 7, 5, 10, 9, 8, 14, 25,
                 11, 3, 1, 0, 2, 16, 41],
        '中国经济持续发展': [10, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 3, 1, 2, 3, 0, 1, 1, 1, 0, 2, 6, 0, 0, 0, 0,
                     0, 0, 4],
        '父辈更好': [4, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 2, 1, 0, 0, 0, 0, 0, 5, 0, 1, 1, 0, 1,
                 4, 4]}, '201606': {
        '健康': [122462, 21348, 18356, 13870, 38560, 18099, 11176, 21437, 31688, 13001, 60648, 52306, 42066, 48558, 23065,
               24800, 88793, 77906, 76018, 41263, 40953, 53229, 27909, 16573, 23932, 28998, 27861, 65218, 178201, 14686,
               8470, 15773, 37632, 4673, 65776, 157821],
        '生活幸福': [15431, 3041, 2931, 2279, 5420, 2974, 1880, 3228, 4483, 1923, 9111, 6913, 5609, 6687, 3584, 3914, 10896,
                 10375, 13090, 5637, 5013, 6505, 4175, 2689, 3145, 3596, 4045, 9083, 21407, 2474, 1573, 1723, 2297, 858,
                 7005, 17839],
        '好工作': [1585, 332, 218, 172, 447, 175, 123, 285, 449, 136, 864, 727, 575, 616, 299, 329, 1253, 1307, 1037, 689,
                1062, 767, 361, 196, 255, 437, 386, 869, 2544, 179, 93, 126, 184, 54, 1126, 2641],
        '家庭幸福': [2361, 426, 442, 347, 760, 413, 257, 535, 754, 252, 1516, 1294, 800, 882, 576, 579, 2057, 1478, 1580,
                 963, 797, 1624, 607, 353, 480, 553, 680, 1359, 3972, 292, 211, 222, 324, 128, 1138, 3760],
        '有房': [2447, 400, 331, 247, 744, 291, 198, 525, 628, 455, 1376, 1054, 1141, 760, 414, 538, 1780, 2743, 1806,
               859, 707, 935, 739, 314, 392, 717, 551, 1348, 3710, 250, 132, 252, 332, 145, 1715, 2793],
        '出名': [4305, 748, 645, 489, 1337, 552, 423, 765, 1085, 364, 2337, 1643, 1264, 1453, 744, 940, 3236, 2836, 2934,
               1718, 1371, 1889, 1041, 639, 800, 1119, 964, 2280, 6442, 477, 264, 376, 679, 212, 3333, 6383],
        '白手起家': [313, 60, 41, 33, 153, 44, 11, 68, 127, 14, 192, 173, 81, 199, 68, 131, 265, 278, 202, 130, 97, 177,
                 109, 48, 59, 66, 88, 187, 516, 34, 11, 37, 35, 15, 179, 540],
        '事业有成': [378, 95, 59, 120, 126, 63, 52, 95, 98, 43, 224, 164, 122, 119, 63, 82, 252, 212, 200, 144, 117, 178,
                 70, 57, 88, 76, 115, 218, 554, 52, 37, 23, 44, 13, 166, 483],
        '发展机会': [1194, 160, 137, 112, 311, 153, 100, 187, 241, 96, 495, 386, 298, 319, 298, 207, 742, 673, 1097, 373,
                 275, 379, 231, 155, 150, 229, 215, 584, 1656, 118, 70, 300, 135, 39, 406, 1528],
        '个体自由': [386, 53, 64, 37, 102, 53, 28, 77, 94, 43, 162, 118, 297, 101, 69, 65, 221, 231, 240, 109, 121, 121,
                 198, 40, 59, 66, 142, 220, 653, 41, 33, 36, 61, 63, 247, 550],
        '收入足够': [70, 6, 6, 4, 18, 5, 1, 3, 3, 2, 30, 15, 9, 7, 9, 10, 34, 21, 26, 16, 14, 9, 7, 9, 9, 13, 11, 23, 72, 3,
                 2, 1, 6, 1, 25, 60],
        '平等机会': [288, 47, 27, 16, 66, 23, 14, 39, 49, 12, 163, 84, 49, 76, 54, 52, 197, 168, 162, 84, 89, 116, 42, 24,
                 33, 51, 48, 101, 301, 15, 10, 16, 28, 7, 283, 348],
        '个人努力': [191, 27, 32, 22, 68, 29, 20, 30, 61, 18, 81, 81, 48, 72, 40, 39, 107, 85, 122, 70, 42, 65, 35, 31, 39,
                 72, 54, 98, 216, 29, 19, 15, 19, 5, 100, 220],
        '祖国强大': [54, 9, 8, 6, 16, 10, 8, 11, 15, 5, 20, 24, 6, 13, 8, 8, 21, 16, 15, 5, 12, 17, 8, 2, 4, 7, 10, 12, 36,
                 8, 2, 2, 1, 2, 17, 63],
        '安享晚年': [118, 33, 21, 17, 57, 16, 14, 23, 53, 16, 91, 89, 74, 63, 29, 37, 117, 109, 96, 57, 58, 60, 44, 20, 36,
                 49, 48, 116, 303, 20, 11, 5, 6, 8, 96, 228],
        '成为富人': [77, 13, 10, 11, 28, 9, 6, 18, 24, 3, 49, 34, 16, 24, 8, 18, 38, 42, 51, 21, 18, 34, 8, 12, 15, 19, 24,
                 26, 100, 5, 6, 5, 4, 4, 40, 100],
        '父辈更好': [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0, 0, 0, 5, 4, 4, 2, 0, 0, 0, 0, 1, 0, 1, 1, 4, 0, 0, 0, 0, 0,
                 4, 3],
        '中国经济持续发展': [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 1, 1, 8, 1, 2, 1, 1, 1, 0, 0, 1, 0, 5, 0, 0, 0, 0,
                     0, 5, 14]}, '201607': {
        '健康': [104315, 19543, 15811, 12532, 33886, 14933, 9691, 21101, 31088, 9113, 54865, 49544, 31726, 43394, 19216,
               23672, 74988, 70978, 67752, 37377, 37442, 46075, 25612, 15072, 20328, 27478, 26233, 58317, 152045, 12602,
               7102, 8578, 16924, 3996, 51851, 131213],
        '生活幸福': [19572, 3746, 3198, 2394, 6042, 3537, 2119, 3678, 5015, 1860, 10246, 8392, 6106, 7963, 4090, 4308,
                 12176, 12561, 12859, 6542, 5759, 7338, 5711, 2910, 3678, 4154, 4387, 8289, 26615, 2671, 1636, 2077,
                 4327, 1103, 7502, 19371],
        '好工作': [1918, 325, 231, 144, 540, 205, 116, 298, 484, 104, 968, 780, 543, 664, 310, 337, 1311, 1269, 1068, 697,
                1002, 741, 371, 212, 646, 364, 445, 833, 2394, 149, 93, 172, 378, 60, 1109, 2353],
        '事业有成': [443, 145, 79, 121, 129, 95, 50, 92, 123, 44, 272, 213, 158, 178, 144, 170, 504, 262, 299, 233, 291,
                 195, 330, 107, 97, 731, 107, 229, 786, 108, 34, 155, 294, 22, 303, 920],
        '发展机会': [1159, 147, 172, 108, 323, 164, 127, 201, 234, 108, 464, 461, 375, 296, 158, 204, 607, 732, 707, 336,
                 339, 329, 226, 152, 167, 230, 251, 615, 1502, 140, 91, 81, 292, 32, 421, 1273],
        '家庭幸福': [2945, 539, 473, 410, 961, 482, 262, 562, 823, 274, 1500, 1327, 953, 969, 539, 652, 1972, 1804, 1856,
                 1038, 939, 1350, 648, 440, 599, 689, 661, 1445, 3641, 458, 267, 288, 509, 123, 1355, 3481],
        '有房': [2440, 486, 350, 268, 985, 314, 239, 494, 696, 632, 1222, 1152, 1197, 769, 425, 469, 1691, 2766, 1799,
               930, 802, 954, 1003, 353, 388, 618, 529, 1269, 3028, 321, 187, 284, 650, 180, 1505, 2611],
        '出名': [4614, 801, 669, 463, 1386, 537, 332, 729, 1097, 350, 2288, 1733, 1256, 1427, 818, 901, 3023, 2809, 2884,
               1781, 1365, 1960, 1047, 598, 779, 1044, 1005, 2323, 5968, 530, 305, 356, 727, 180, 3022, 6050],
        '白手起家': [371, 77, 43, 38, 156, 52, 30, 90, 121, 21, 280, 213, 148, 122, 57, 94, 310, 324, 272, 161, 131, 151,
                 128, 70, 80, 102, 104, 186, 653, 50, 24, 38, 92, 11, 273, 555],
        '个人努力': [168, 24, 35, 23, 56, 35, 18, 46, 50, 16, 73, 62, 50, 53, 36, 37, 106, 82, 109, 39, 51, 72, 41, 33, 25,
                 113, 31, 71, 247, 31, 19, 8, 26, 4, 74, 168],
        '祖国强大': [135, 33, 17, 14, 49, 26, 11, 33, 33, 9, 72, 56, 46, 55, 14, 22, 71, 71, 84, 54, 34, 47, 42, 14, 22, 27,
                 26, 63, 142, 15, 7, 5, 10, 4, 99, 214],
        '个体自由': [309, 52, 49, 41, 107, 58, 39, 65, 97, 37, 149, 97, 285, 104, 70, 72, 219, 189, 251, 108, 106, 121, 357,
                 39, 62, 102, 141, 260, 378, 54, 22, 25, 54, 74, 291, 479],
        '平等机会': [275, 41, 36, 23, 65, 24, 16, 37, 61, 21, 129, 81, 62, 68, 37, 47, 179, 172, 183, 81, 62, 114, 57, 27,
                 33, 41, 48, 117, 375, 28, 16, 21, 35, 9, 166, 346],
        '安享晚年': [113, 20, 24, 15, 48, 20, 15, 19, 39, 10, 68, 65, 42, 38, 25, 35, 112, 122, 100, 66, 76, 67, 28, 22, 28,
                 50, 59, 109, 189, 10, 14, 12, 8, 4, 137, 204],
        '成为富人': [112, 20, 17, 17, 30, 16, 14, 24, 26, 9, 72, 50, 29, 27, 17, 19, 88, 79, 96, 35, 27, 47, 29, 11, 21, 23,
                 23, 54, 127, 14, 12, 15, 9, 5, 70, 112],
        '收入足够': [94, 12, 6, 7, 10, 3, 5, 16, 12, 3, 30, 16, 13, 13, 5, 8, 34, 30, 49, 17, 20, 25, 12, 3, 3, 14, 14, 25,
                 59, 7, 5, 6, 4, 3, 28, 73],
        '中国经济持续发展': [4, 0, 0, 0, 0, 1, 0, 0, 1, 1, 4, 0, 0, 0, 0, 0, 2, 2, 3, 2, 1, 3, 0, 0, 0, 0, 1, 2, 4, 0, 0, 0, 0,
                     0, 1, 14],
        '父辈更好': [5, 1, 0, 0, 3, 2, 0, 1, 2, 0, 2, 3, 3, 0, 0, 0, 5, 1, 0, 3, 0, 0, 2, 0, 1, 0, 2, 1, 5, 0, 0, 0, 1, 0,
                 0, 3]}, '201608': {
        '健康': [60700, 10231, 9109, 7656, 20763, 9315, 5484, 12393, 17987, 5583, 32021, 28705, 18795, 26655, 10590,
               13698, 44035, 39698, 35909, 21216, 21363, 26694, 13006, 8941, 12196, 16450, 14623, 31184, 84047, 7589,
               3943, 4991, 6881, 2275, 29676, 79735],
        '生活幸福': [9279, 1793, 1584, 1232, 3151, 1461, 894, 1949, 2476, 868, 5311, 4573, 3123, 3787, 1750, 2077, 6254,
                 5547, 5443, 3441, 2759, 3745, 2906, 1336, 1755, 2149, 2124, 4405, 12112, 1166, 814, 1024, 1337, 470,
                 3905, 10553],
        '有房': [1887, 468, 245, 167, 603, 235, 136, 324, 492, 491, 974, 741, 831, 541, 309, 327, 1298, 1842, 1487, 615,
               575, 722, 709, 232, 307, 540, 366, 1012, 2256, 184, 102, 115, 182, 80, 1177, 2215],
        '好工作': [849, 164, 102, 63, 291, 127, 63, 158, 253, 77, 455, 453, 262, 290, 134, 149, 604, 525, 531, 350, 634,
                394, 163, 103, 136, 194, 179, 399, 1106, 72, 43, 60, 101, 27, 605, 1139],
        '家庭幸福': [1778, 309, 291, 243, 721, 280, 159, 375, 499, 182, 1090, 839, 554, 609, 353, 397, 1222, 977, 998, 674,
                 564, 792, 353, 242, 359, 459, 421, 911, 2303, 231, 152, 152, 179, 78, 777, 2207],
        '出名': [3359, 648, 415, 342, 874, 396, 245, 448, 703, 216, 1523, 1190, 832, 861, 480, 632, 1920, 1819, 1783, 894,
               826, 1165, 694, 407, 475, 680, 623, 1570, 3768, 347, 208, 214, 312, 124, 1818, 4189],
        '发展机会': [785, 85, 76, 88, 192, 95, 70, 108, 134, 54, 281, 260, 156, 188, 95, 102, 318, 374, 552, 190, 280, 198,
                 82, 86, 90, 158, 125, 293, 944, 56, 47, 33, 68, 18, 231, 673],
        '白手起家': [210, 37, 34, 15, 82, 30, 18, 42, 63, 19, 109, 102, 64, 60, 32, 30, 146, 141, 122, 73, 75, 98, 45, 28,
                 53, 50, 50, 118, 301, 32, 12, 25, 23, 8, 136, 283],
        '成为富人': [81, 8, 17, 9, 19, 9, 8, 22, 11, 7, 35, 34, 23, 17, 8, 11, 31, 32, 43, 25, 15, 27, 10, 8, 15, 12, 11,
                 34, 70, 8, 7, 3, 4, 3, 21, 48],
        '事业有成': [237, 75, 35, 34, 87, 42, 23, 45, 72, 17, 154, 94, 77, 89, 45, 41, 153, 150, 125, 79, 65, 110, 51, 30,
                 46, 49, 70, 149, 321, 32, 16, 18, 23, 10, 141, 337],
        '个体自由': [263, 36, 26, 15, 65, 19, 18, 25, 57, 16, 75, 85, 159, 55, 43, 42, 132, 131, 165, 51, 47, 80, 488, 28,
                 36, 46, 48, 92, 231, 23, 16, 14, 41, 30, 150, 311],
        '平等机会': [135, 20, 11, 14, 31, 14, 5, 13, 36, 2, 66, 43, 24, 36, 15, 24, 84, 49, 69, 58, 30, 40, 25, 7, 14, 20,
                 30, 58, 160, 7, 8, 11, 15, 6, 75, 166],
        '祖国强大': [61, 9, 9, 9, 22, 9, 4, 20, 15, 5, 37, 24, 18, 20, 17, 14, 46, 27, 29, 25, 20, 28, 20, 15, 14, 13, 18,
                 34, 57, 13, 3, 3, 1, 1, 27, 90],
        '安享晚年': [77, 6, 11, 6, 13, 14, 14, 14, 18, 6, 28, 48, 28, 25, 13, 29, 61, 70, 67, 38, 28, 42, 28, 22, 12, 31,
                 26, 63, 129, 10, 8, 1, 10, 0, 40, 109],
        '个人努力': [96, 17, 12, 10, 26, 13, 5, 19, 35, 10, 55, 39, 24, 27, 16, 21, 53, 35, 41, 30, 30, 21, 19, 8, 13, 64,
                 15, 35, 89, 6, 4, 4, 7, 1, 36, 98],
        '收入足够': [67, 13, 1, 4, 13, 3, 3, 8, 12, 3, 19, 11, 13, 15, 4, 6, 48, 33, 65, 20, 13, 27, 11, 3, 3, 19, 5, 53,
                 76, 4, 4, 3, 3, 0, 40, 73],
        '中国经济持续发展': [5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 13, 2, 3, 0, 0, 0, 3, 7, 3, 0, 0, 2, 1, 0, 1, 0, 2, 0, 4, 0, 0, 1, 0,
                     0, 3, 5],
        '父辈更好': [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 2, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                 1, 2]}, '201609': {
        '健康': [80974, 13961, 11899, 9613, 30058, 23426, 8040, 15575, 21676, 9788, 38937, 33875, 31936, 35554, 15773,
               18047, 54095, 45974, 42882, 33757, 30755, 34596, 28064, 10938, 15307, 21684, 17904, 35019, 107301, 16502,
               5931, 6689, 9545, 4079, 33454, 83262],
        '家庭幸福': [2648, 484, 495, 446, 897, 473, 362, 548, 857, 397, 1424, 1219, 880, 860, 575, 658, 1645, 1428, 1420,
                 987, 875, 1176, 576, 485, 521, 672, 685, 1481, 3744, 405, 296, 310, 343, 173, 1119, 2628],
        '生活幸福': [10636, 2146, 2240, 1584, 3663, 1906, 1298, 2207, 2995, 1357, 5592, 4828, 3412, 5034, 2301, 2524, 6687,
                 6346, 7106, 3990, 3521, 4288, 2968, 1755, 2173, 2599, 2724, 5420, 14710, 1696, 1111, 1273, 1621, 785,
                 5272, 11251],
        '事业有成': [277, 61, 51, 29, 78, 34, 26, 51, 67, 23, 155, 118, 73, 87, 53, 63, 166, 229, 166, 99, 95, 122, 50, 37,
                 46, 45, 51, 98, 361, 25, 25, 27, 38, 10, 131, 326],
        '出名': [3082, 506, 456, 339, 883, 369, 290, 453, 726, 300, 1469, 1006, 781, 923, 489, 549, 1957, 1701, 1977, 977,
               807, 1130, 682, 402, 509, 720, 598, 1250, 3880, 328, 187, 294, 402, 163, 1758, 3616],
        '有房': [2708, 512, 385, 328, 844, 348, 241, 480, 612, 522, 1299, 996, 836, 746, 457, 510, 1590, 2217, 1972, 783,
               666, 1029, 709, 356, 474, 636, 483, 1134, 2664, 355, 247, 261, 315, 185, 1473, 2488],
        '好工作': [1047, 186, 129, 105, 329, 142, 86, 208, 344, 120, 531, 592, 361, 334, 203, 267, 723, 949, 620, 369, 621,
                529, 212, 185, 212, 257, 229, 440, 1273, 128, 69, 83, 111, 52, 604, 1384],
        '发展机会': [897, 130, 148, 124, 242, 155, 133, 143, 226, 140, 432, 313, 190, 223, 141, 176, 417, 358, 454, 238,
                 229, 311, 145, 150, 172, 194, 169, 410, 966, 145, 91, 101, 93, 62, 291, 733],
        '安享晚年': [117, 21, 18, 11, 31, 12, 7, 17, 42, 11, 72, 49, 50, 34, 27, 24, 94, 80, 70, 43, 48, 70, 28, 12, 21, 40,
                 27, 55, 169, 13, 5, 6, 4, 5, 52, 106],
        '个人努力': [81, 7, 9, 9, 16, 9, 7, 10, 25, 2, 29, 31, 19, 191, 18, 15, 45, 34, 47, 20, 24, 22, 9, 14, 12, 27, 18,
                 31, 67, 8, 11, 6, 7, 6, 45, 84],
        '个体自由': [223, 55, 57, 53, 120, 42, 40, 54, 71, 35, 97, 91, 110, 95, 62, 60, 137, 128, 183, 74, 66, 80, 463, 40,
                 44, 71, 83, 96, 254, 33, 39, 35, 37, 44, 122, 305],
        '白手起家': [223, 51, 35, 28, 74, 32, 20, 42, 68, 20, 158, 175, 52, 88, 55, 45, 175, 180, 145, 104, 68, 106, 42, 40,
                 51, 65, 68, 115, 398, 21, 12, 22, 21, 7, 138, 253],
        '祖国强大': [51, 11, 10, 7, 20, 10, 9, 11, 20, 7, 30, 37, 13, 24, 9, 9, 32, 32, 25, 18, 13, 27, 11, 7, 16, 14, 13,
                 26, 47, 6, 2, 6, 6, 1, 23, 82],
        '成为富人': [76, 10, 16, 15, 24, 8, 13, 15, 19, 12, 56, 32, 29, 21, 20, 17, 34, 44, 37, 31, 28, 26, 22, 21, 9, 21,
                 11, 41, 110, 9, 4, 6, 10, 14, 20, 96],
        '收入足够': [37, 1, 4, 0, 4, 5, 1, 3, 13, 2, 11, 14, 7, 11, 3, 3, 12, 15, 22, 6, 9, 10, 10, 5, 5, 3, 5, 10, 53, 0,
                 1, 1, 4, 0, 23, 34],
        '中国经济持续发展': [47, 6, 3, 4, 19, 3, 0, 10, 8, 1, 38, 19, 9, 14, 5, 14, 41, 32, 35, 11, 18, 24, 9, 4, 3, 8, 10, 17,
                     79, 4, 0, 1, 0, 1, 21, 51],
        '平等机会': [119, 14, 6, 5, 19, 15, 6, 12, 11, 5, 39, 23, 16, 21, 6, 17, 50, 44, 64, 35, 23, 43, 13, 10, 12, 19, 9,
                 28, 103, 7, 7, 4, 7, 6, 59, 126],
        '父辈更好': [3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0,
                 1, 2]}}

    for current_file in file_paht_list:
        print(current_file)
        with open(current_file, 'r', encoding='utf-8') as f:
            current_time = current_file.split('/')[-1].split('.')[0]
            print(current_time)
            if (current_time in output_dic.keys()):
                    continue
            output_dic[current_time] = {}
            s_t = time()
            for line in f:
                line_section = line.split('\t')
                current_text = getText(line_section)
                # dismiss weibo which is too short(<5)
                current_text = filer.filer(current_text)
                word_list = [word for word in jieba.cut(current_text)]
                if (len(word_list) < 5):
                    continue

                location = getLocation(line_section)
                if(len(location) == 0):
                    continue
                current_city_list = location.split()
                if(len(current_city_list) == 0):
                    continue
                current_city = current_city_list[0]
                keyword_list = getKeywordList(line_section)

                # 统计所有
                for keyword in keyword_list:
                    keyword = keyword.replace(',', '')
                    if (keyword not in output_dic[current_time].keys()):
                        print(keyword)
                        output_dic[current_time][keyword] = [0 for i in range(len(city_list))]
                    output_dic[current_time][keyword][city_list.index(current_city)] += 1

            e_t = time()
            print('current file process time: ' + str(e_t - s_t))
            print(output_dic)

#待组装
# keywords_list = ['健康','事业有成','发展机会','生活幸福','有房','出名','家庭幸福','好工作','平等机会','白手起家','成为富人','个体自由','安享晚年','收入足够','个人努力','祖国强大','中国经济持续发展','父辈更好']
def keyword_emotion_time(file_paht_list):
    output_dic = {}
    for current_file in file_paht_list:
        print(current_file)
        with open(current_file, 'r', encoding='utf-8') as f:
            current_time = current_file.split('/')[-1].split('.')[0]
            print(current_time)
            output_dic[current_time] = {}
            s_t = time()
            for line in f:
                line_section = line.split('\t')
                current_text = getText(line_section)
                # dismiss weibo which is too short(<5)
                current_text = filer.filer(current_text)
                word_list = [word for word in jieba.cut(current_text)]
                if (len(word_list) < 5):
                    continue

                location = getLocation(line_section)
                current_city = location.split()[0]
                keyword_list = getKeywordList(line_section)

                # 统计所有
                for keyword in keyword_list:
                    keyword = keyword.replace(',', '')
                    if (keyword not in output_dic[current_time].keys()):
                        print(keyword)
                        output_dic[current_time][keyword] = [0 for i in range(len(city_list))]
                    output_dic[current_time][keyword][city_list.index(current_city)] += 1

            e_t = time()
            print('current file process time: ' + str(e_t - s_t))
            print(output_dic)

def keyword_emotion(file_paht_list):
    output_dic = {}
    for current_keyword in keywords_list:
        output_dic[current_keyword] = {}
    for current_file in file_paht_list:
        print(current_file)
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')
                current_text = getText(line_section)
                # dismiss weibo which is too short(<5)
                current_text = filer.filer(current_text)
                word_list = [word for word in jieba.cut(current_text)]
                if (len(word_list) < 5):
                    continue
                mood = getMood(line_section)
                keyword_list = getKeywordList(line_section)

                # 统计所有
                for keyword in keyword_list:
                    keyword = keyword.replace(',', '')
                    if (str(mood) not in output_dic[keyword].keys()):
                        output_dic[keyword][str(mood)] = 0
                    else:
                        output_dic[keyword][str(mood)] += 1

            e_t = time()
            print('current file process time: ' + str(e_t - s_t))
            print(output_dic)

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

