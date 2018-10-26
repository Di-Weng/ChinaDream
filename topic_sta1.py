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
from gensim.models import LdaModel
from gensim.models import LdaMulticore
import codecs
from collections import defaultdict

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

#按省份划分collection
def conntoMongoWeiboProvince(ServerURL = '127.0.0.1'):
    conn = pymongo.MongoClient(ServerURL,
                   27017,
                   username='wd',
                   password='wd123456',
                  )
    # db = conn.weiboProvince_text
    db = conn.weiboProvince
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

def classify_Province(file_path_list, usingMongo = 1):
    # usingMongo 0 代表使用文件存储；1代表使用MongoDB存储
    dismiss = 0
    existing_province = set()
    if (not usingMongo):
        weiboprovincefilefolder = 'D:/chinadream/province/'
        for current_file in file_path_list:
            with open(current_file, 'r', encoding='utf-8') as f:
                s_t = time()
                for line in f:
                    line_section = line.split('\t')

                    location = getLocation(line_section)
                    if(len(location) == 0):
                        dismiss += 1
                        continue
                    current_province = location.split()[0]
                    write_file_path = weiboprovincefilefolder + current_province + '.txt'
                    write_file = open(write_file_path,'a+', encoding = 'utf-8')
                    write_file.write(line)
                    write_file.write('\n')
                    # print(current_province)
            e_t = time()
            print(existing_province)
            print('dismiss count: ' + str(dismiss))
            print('current collection' + str(current_file) + 'process time: ' + str(e_t - s_t))
    else:
        db = conntoMongoWeiboProvince()
        for current_file in file_path_list:
            with open(current_file, 'r', encoding='utf-8') as f:
                s_t = time()
                for line in f:
                    line_section = line.split('\t')
                    json_data = line_section[-1].strip()
                    location = getLocation(line_section)
                    if (len(location) == 0):
                        dismiss += 1
                        continue
                    current_province = location.split()[0]
                    data_toinsert ={
                        'location':location,
                        'line': json_data
                    }
                    current_collection = db[current_province]
                    result = current_collection.insert_one(data_toinsert)
            e_t = time()
            print(existing_province)
            print('dismiss count: ' + str(dismiss))
            print('current file:\t' + str(current_file) + '\tprocess time:\t' + str(e_t - s_t))

#有待组装
def keyword_lda(mongo_server = '127.0.0.1',usingMongo = 1):
    jieba.load_userdict("data/user_dict.txt")
    stop_word = []
    weibocityfilefolder = 'D:/chinadream/city/'
    with open('data/stop_word.txt', 'r', encoding='utf-8') as sw_f:
        for item in sw_f:
            stop_word.append(item.strip())

    if(not usingMongo):
        city_folder = 'D:/chinadream/city/'
        folderlist = os.listdir(city_folder)
        for current_city in folderlist:
            origin_text = []
            open_city_file = open(weibocityfilefolder+current_city,'r',encoding='utf-8')
            for temp_line in open_city_file:
                weibo_origin = filer.filer(temp_line).replace('/','')
                if (len(weibo_origin) == 0):
                    continue
                weibo_cut = list(jieba.cut(weibo_origin))
                weibo_cut_list = []
                for items in weibo_cut:
                    if (items not in stop_word and len(items.strip()) > 0):
                        weibo_cut_list.append(items)
                if(len(weibo_cut_list) < 5):
                    continue
                origin_text.append(weibo_cut_list)

            frequency = defaultdict(int)
            for text in origin_text:
                for token in text:
                    frequency[token] += 1
            texts = [[token for token in text if frequency[token] > 1]
                     for text in origin_text]
            print(texts)

            word_count_dict = corpora.Dictionary(texts)
            corpus = [word_count_dict.doc2bow(text) for text in texts]
            print(corpus)
            corpora.MmCorpus.serialize('data/topic/' + current_city + '_mmcorpus.mm',
                                       corpus)  # store to disk, for later use
            lda = LdaMulticore(corpus=corpus, id2word=word_count_dict, num_topics=50, workers=7)
            topics_r = lda.print_topics(20)
            lda.get_document_topics()
            print(topics_r)
            # print(topics_r)
            print('____________')
            topic_name = codecs.open('result/topic/' + current_city + '_topics_result.txt', 'w',
                                     encoding='utf-8')
            for v in topics_r:
                topic_name.write(str(v) + '\n')
            topic_name.close()
        return
    else:
        print('using mongo')
        # db = conntoMongoWeiboProvince(mongo_server)
        # for current_connection_name in db.collection_names():
        #     origin_text = []
        #     word_set = set()
        #     print(current_connection_name)
        #     current_connection = db[current_connection_name]
        #     query_cursor = current_connection.find()
        #     for mongo_doc in query_cursor:
        #         json_file = mongo_doc['line']
        #         dic_file = json.loads(json_file)
        #         weibo_origin = dic_file['text']
        #         weibo_origin = filer.filer(weibo_origin).replace('/','')
        #         if (len(weibo_origin) == 0):
        #             continue
        #         weibo_cut = list(jieba.cut(weibo_origin))
        #         weibo_cut_list = []
        #         for items in weibo_cut:
        #             if (items not in stop_word and len(items.strip()) > 0):
        #                 weibo_cut_list.append(items)
        #         if(len(weibo_cut_list) < 5):
        #             continue
        #         origin_text.append(weibo_cut_list)
        #
        #     frequency = defaultdict(int)
        #     for text in origin_text:
        #         for token in text:
        #             frequency[token] += 1
        #     texts = [[token for token in text if frequency[token] > 1]
        #              for text in origin_text]
        #     print(texts)
        #
        #     word_count_dict = corpora.Dictionary(texts)
        #     corpus = [word_count_dict.doc2bow(text) for text in texts]
        #     print(corpus)
        #     corpora.MmCorpus.serialize('data/topic/' + current_connection_name+ '_mmcorpus.mm', corpus)  # store to disk, for later use
        #     lda = LdaMulticore(corpus=corpus, id2word=word_count_dict, num_topics=50,workers=7)
        #     topics_r = lda.print_topics(20)
        #     print(topics_r)
        #     # print(topics_r)
        #     print('____________')
        #     topic_name = codecs.open('result/topic/' + current_connection_name +'_topics_result.txt', 'w',encoding='utf-8')
        #     for v in topics_r:
        #         topic_name.write(str(v) + '\n')
        #     topic_name.close()

# weibofilefolder = 'D:/chinadream/data'
# 按时间-中国梦维度-市（区）存储文件
# 按中国梦维度-市(区)存储文件
def collect_city_file(file_path_list):
    ignore_region = ['其他','海外']
    output_file_1 = 'D:/chinadream/keyword_location/'
    output_file_2 = 'D:/chinadream/time_keyword_location/'
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

