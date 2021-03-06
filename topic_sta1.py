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
from math import sqrt
from filer import remove_at
import fcntl

# the uppest path of weibo data document
weibofilefolder = '/Volumes/data/chinadream/data'
north_city = ['北京','天津','内蒙古','新疆','河北','甘肃','宁夏','山西','陕西','青海','山东','河南','安徽','辽宁','吉林','黑龙江']
south_city = ['江苏','浙江','上海','湖北','湖南','四川','重庆','贵州','云南','广西','江西','福建','广东','海南','西藏','台湾','香港','澳门']
# return [filepath]
def getAllFile(folderpath):
    temp_list = []
    folderlist = os.listdir(folderpath)
    temp_list = [folderpath + '/' + filename + '/' + filename for filename in folderlist if filename != '.DS_Store']
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

def getisSpam(line_section):
    if(type(line_section) == list):
        temp_dic_str = line_section[-1].strip()
        temp_dic = json.loads(temp_dic_str)
        return temp_dic['is_spam']
    elif(type(line_section) == dict):
        return(line_section['is_spam'])
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
    weibocityfilefolder = '/Volumes/data/chinadream/city/'

    # keyword_finished = []
    # db = conntoMongoKeywordLocation_topic()
    # for keyword_result in db['topic'].find():
    #     keyword_finished.append(keyword_result['keyword'])

    with open('data/stop_word.txt', 'r', encoding='utf-8') as sw_f:
        for item in sw_f:
            stop_word.append(item.strip())

    keyword_folder = '/Volumes/data/chinadream/keyword_location/'
    folderlist = os.listdir(keyword_folder)
    for current_keyword in folderlist:
        # if(current_keyword in keyword_finished):
        #     continue
        print(current_keyword)
        current_keyword_folder = keyword_folder + current_keyword + '/'
        current_keyword_cut_list = current_keyword.split(',')
        current_keyword_banned_list = []
        if(current_keyword == '个人努力' or current_keyword == '健康' or (not os.listdir(current_keyword_folder))):
            continue
        # 全切
        for temp1 in current_keyword_cut_list:
            cut_list = jieba.cut(temp1)
            for temp2 in cut_list:
                current_keyword_banned_list.append(temp2)


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

# 某年某个中国梦的所有情感(默认)下的 关于市（直辖市的区）级的LDA
def year_keyword_location_lda(current_year,current_keyword,mood_list = 'all'):
    jieba.load_userdict("data/user_dict.txt")
    stop_word = []

    with open('data/stop_word.txt', 'r', encoding='utf-8') as sw_f:
        for item in sw_f:
            stop_word.append(item.strip())
    current_keyword_cut_list = current_keyword.split(',')
    current_keyword_banned_list = []
    # 全切
    for temp1 in current_keyword_cut_list:
        cut_list = jieba.cut(temp1)
        for temp2 in cut_list:
            current_keyword_banned_list.append(temp2)

    time_keyword_folder = '/Volumes/data/chinadream/time_keyword_emotion_location'
    timemonth_list = os.listdir(time_keyword_folder)
    current_year_timemonth_list = []
    for current_timemonth in timemonth_list:
        if(current_timemonth[0:4] == str(current_year)):
            current_year_timemonth_list.append(current_timemonth)

    corpus_text = []
    corpus_city = {}
    count = 0
    print('开始抽取语料')
    for current_timemonth in current_year_timemonth_list:
        if(mood_list == 'all'):
            current_mood_path = time_keyword_folder+'/'+current_timemonth
            current_mood_list = os.listdir(current_mood_path)
            for current_mood in current_mood_list:
                if(current_mood == '.DS_Store'):
                    continue
                current_folder_keyword_list = os.listdir(current_mood_path + '/' + str(current_mood))
                if(current_keyword not in current_folder_keyword_list):
                    continue

                current_city_path = current_mood_path + '/' + str(current_mood) + '/' + current_keyword
                current_city_list = os.listdir(current_city_path)

                for current_city in current_city_list:
                    if(current_city == '.DS_Store'):
                        continue
                    if(current_city in corpus_city):
                        city_index = corpus_city[current_city]
                        origin_text = corpus_text[city_index]
                    else:
                        origin_text = []

                    current_city_file_path = current_city_path + '/' +current_city
                    for temp_line in open(current_city_file_path):
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
                    # 该城市没有符合条件的预料被抽取
                    if (len(origin_text) == 0):
                        continue
                    if (current_city in corpus_city):
                        # 更新语料
                        corpus_text[city_index] = origin_text
                    else:
                        #添加语料，更新index
                        corpus_text.append(origin_text)
                        corpus_city[current_city] = count
                        count += 1
    #释放内存
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
    lda = LdaModel(corpus=corpus_tfidf, id2word=word_count_dict, num_topics=100)
    output_model_folder = 'data/year_keyword_location_lda/model/' + str(current_year) + '_' + current_keyword + '_' + mood_list
    if (not os.path.exists(output_model_folder)):
        os.makedirs(output_model_folder)
    model_file = output_model_folder + '/' + str(current_year) + '_' + current_keyword + '_' + mood_list  + '_lda.model'
    dictionary_file = output_model_folder + '/' + str(current_year) + '_' + current_keyword + '_' + mood_list  + '_lda.dict'
    corpus_file = output_model_folder + '/' + str(current_year) + '_' + current_keyword + '_' + mood_list  + '_lda.mm'
    word_count_dict.save(dictionary_file)
    corpora.MmCorpus.serialize(corpus_file,corpus)
    lda.save(model_file)

    # db = conntoMongoKeywordLocation_topic()
    # current_collection = db[collection_name_1]
    # data_toinsert = {
    #     'topic_distri':'1',
    #     'keyword': current_keyword,
    #     'all_topic': str(lda.print_topics(-1))
    # }
    # result = current_collection.insert_one(data_toinsert)

    # write to file
    output_folder = 'result/year_keyword_location_lda/' + str(current_year) + '_' + current_keyword + '_' + mood_list
    if (not os.path.exists(output_folder)):
        os.makedirs(output_folder)

    #默认20个话题
    lda_topic_list = lda.print_topics()
    with open(output_folder + '/lda_topics.txt', 'a+', encoding='utf-8') as output_file:
        output_file.write(str(current_year) + '_' + current_keyword + '_' + mood_list)
        output_file.write('\n')
        for current_topic in lda_topic_list:
            output_file.write(str(current_topic))
            output_file.write('\n')

    for city_name, city_index in corpus_city.items():
        city_corpus = corpus[city_index]
        doc_lda = lda.get_document_topics(city_corpus)  # 得到新文档的主题分布
        # print(doc_lda)

        # db = conntoMongoKeywordLocation()
        # collection_name_1 = str(current_year) + '_' + current_keyword + '_' + mood_list
        # current_collection = db[collection_name_1]
        # data_toinsert = {
        #     'city': city_name,
        #     'topic_distribution': str(doc_lda)
        # }
        # result = current_collection.insert_one(data_toinsert)


        with open(output_folder + '/city_topics.txt', 'a+', encoding='utf-8') as output_file:
            output_city_name = city_name.split('.')[0]
            output_file.write(output_city_name)
            output_file.write('\n')
            output_file.write(str(doc_lda))
            output_file.write('\n')

    return

# weibofilefolder = '/Volumes/data/chinadream/data'
# 按时间-中国梦维度-市（区）存储文件
# 按中国梦维度-市(区)存储文件
def collect_city_file(file_path_list):
    ignore_region = ['其他','海外']
    output_file_1 = '/Volumes/data/chinadream/keyword_location/'
    output_file_2 = '/Volumes/data/chinadream/time_keyword_location/'
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

# weibofilefolder = '/Volumes/data/chinadream/data'
mood_list = ['愤怒','厌恶','高兴','悲伤','恐惧']
# 按时间-中国梦维度-情感-市（区）存储文件
# 按中国梦维度-情感-市(区)存储文件
def collect_time_emotion_city_file(file_path_list):
    ignore_region = ['其他','海外']
    output_file_1 = '/Volumes/data/chinadream/keyword_emotion_location/'

    for current_file in file_path_list:
        line_count = 0
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            f_t = 0
            nf_t = 0
            for line in f:
                t_1 = time()
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
                    current_out_path_1 = output_file_1 + str(current_mood) + '/' + current_keyword
                    # print(current_out_path_1)
                    if(not os.path.exists(current_out_path_1)):
                        os.makedirs(current_out_path_1)

                    keyword_location_file = open(current_out_path_1 + '/' + city + '.txt', 'a+', encoding='utf-8')
                    keyword_location_file.write(current_text)
                    keyword_location_file.write('\n')
                    keyword_location_file.close()

            e_t = time()
        log_file.close()
        print('current_file:' + current_file)
        print('current file process time: ' + str(e_t - s_t))
    return 1

def multi_collect_time_emotion_city_file(current_file):
    ignore_region = ['其他','海外']
    output_file_2 = '/Volumes/data/chinadream/time_keyword_emotion_location/'
    if(current_file=='.DS_Store'):
        return 1
    print(current_file)
    line_count = 0
    with open(current_file, 'r', encoding='utf-8') as f:
        s_t = time()
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
            log_file = open('/Volumes/data/chinadream/log/' + time_stamp + '.txt', 'w+', encoding='utf-8')
            log_file.write(str(line_count))
            for current_keyword in current_keyword_list:
                if(current_keyword=='.DS_Store'):
                    continue
                temp1 = current_file.split('/')[-1]
                temp2 = temp1.split('.')[0]
                current_out_path_2_time = output_file_2 + temp2 + '/' + str(current_mood)
                if(not os.path.exists(current_out_path_2_time)):
                    os.makedirs(current_out_path_2_time)

                current_out_path_2_time_keyword = current_out_path_2_time + '/' + current_keyword

                if(not os.path.exists(current_out_path_2_time_keyword)):
                    os.mkdir(current_out_path_2_time_keyword)
                time_keyword_location_file = open(current_out_path_2_time_keyword + '/' + city + '.txt', 'a+', encoding='utf-8')
                time_keyword_location_file.write(current_text)
                time_keyword_location_file.write('\n')
                time_keyword_location_file.close()
        e_t = time()
    print('current_file:' + current_file)
    print('current file process time: ' + str(e_t - s_t))
    return 1

def multi_collect_time_emotion_city_file_nospam(current_file):
    ignore_region = ['其他','海外']
    output_file_2 = '/Volumes/data/chinadream/time_keyword_emotion_location_nospams/'
    if(current_file=='.DS_Store'):
        return 1
    print(current_file)
    line_count = 0
    with open(current_file, 'r', encoding='utf-8') as f:
        s_t = time()
        for line in f:
            line_section = line.split('\t')
            current_text = getText(line_section)
            current_isspam = getisSpam(line_section)
            current_keyword_list = getKeywordList(line_section)
            current_detailed_location = getLocation(line_section)
            current_location_list = current_detailed_location.split()
            current_mood = getMood(line_section)
            if(len(str(current_mood)) == 0 ):
                continue
            if (current_isspam == 1):
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
            log_file = open('/Volumes/data/chinadream/log_nospams/' + time_stamp + '.txt', 'w+', encoding='utf-8')
            log_file.write(str(line_count))
            for current_keyword in current_keyword_list:
                if(current_keyword=='.DS_Store'):
                    continue
                temp1 = current_file.split('/')[-1]
                temp2 = temp1.split('.')[0]
                current_out_path_2_time = output_file_2 + temp2 + '/' + str(current_mood)
                if(not os.path.exists(current_out_path_2_time)):
                    os.makedirs(current_out_path_2_time)

                current_out_path_2_time_keyword = current_out_path_2_time + '/' + current_keyword

                if(not os.path.exists(current_out_path_2_time_keyword)):
                    os.mkdir(current_out_path_2_time_keyword)
                time_keyword_location_file = open(current_out_path_2_time_keyword + '/' + city + '.txt', 'a+', encoding='utf-8')
                time_keyword_location_file.write(current_text)
                time_keyword_location_file.write('\n')
                time_keyword_location_file.close()
        e_t = time()
    print('current_file:' + current_file)
    print('current file process time: ' + str(e_t - s_t))
    return 1

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
            s_t = time()
            current_time = current_file.split('/')[-1].split('.')[0]
            print(current_time)
            if (current_time in output_dic.keys()):
                    continue
            output_dic[current_time] = {}
            for current_keyword in keywords_list:
                output_dic[current_time][current_keyword] = {}
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
                    if (str(mood) not in output_dic[current_time][keyword].keys()):
                        output_dic[current_time][keyword][str(mood)] = 0
                    else:
                        output_dic[current_time][keyword][str(mood)] += 1
            e_t = time()
            print('current file process time: ' + str(e_t - s_t))
            print(output_dic)
    return output_dic

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
    return output_dic

# output['at'] = [按照keyword顺序统计]
# output['repost'] = [按照keyword顺序统计]
# output['at_total'] = 所有微博数
# output['repost_total'] = 所有微博数
def keyword_mentionrepost(file_paht_list):
    dismiss_count = 0
    all_keywords_list = ['健康', '事业有成', '发展机会', '生活幸福', '有房', '出名', '家庭幸福', '好工作', '平等机会', '白手起家', '成为富人', '个体自由', '安享晚年',
                     '收入足够', '个人努力', '祖国强大', '中国经济持续发展', '父辈更好']

    output_dic = {}
    output_dic['at'] = [0 for i in all_keywords_list]
    output_dic['at_total'] = [0 for i in all_keywords_list]
    output_dic['repost'] = [0 for i in all_keywords_list]
    output_dic['repost_total'] = [0 for i in all_keywords_list]

    print(output_dic)
    for current_file in file_paht_list:
        with open(current_file, 'r', encoding='utf-8') as f:
            s_t = time()
            for line in f:
                line_section = line.split('\t')
                location = getLocation(line_section)
                keyword_list = getKeywordList(line_section)
                current_text = getText(line_section)

                current_text = filer.filer(current_text)

                #先统计@率和转发率再移除@的符号
                current_at = current_text.count('@')
                current_repost = current_text.count('//')

                current_text = remove_at(current_text)

                word_list = [word for word in jieba.cut(current_text)]
                if (len(word_list) < 5):
                    dismiss_count += 1
                    continue

                for keyword in keyword_list:
                    keyword = keyword.replace(',', '')
                    output_dic['at'][all_keywords_list.index(keyword)] += current_at
                    output_dic['at_total'][all_keywords_list.index(keyword)] += 1
                    output_dic['repost'][all_keywords_list.index(keyword)] += current_repost
                    output_dic['repost_total'][all_keywords_list.index(keyword)] += 1
            e_t = time()
        print(output_dic)
        print('dismiss count: ' + str(dismiss_count))
        print('current collection process time: ' + str(e_t - s_t))

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

