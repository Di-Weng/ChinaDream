# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2018/10/22 20:00
   Author  : diw
   Email   : di.W@hotmail.com
   File    : keyword_location_lda.py
   Desc:
-------------------------------
"""
import topic_sta1
import os
import jieba
import filer
from nltk import FreqDist
from gensim import models
from gensim.corpora import Dictionary
import matplotlib
import codecs

def merege_iter(dic_out,freq_item):
    outdic = {}
    for keyword,keyword_count in dic_out.items():
        outdic[keyword] = keyword_count
    for keyword,keyword_count in freq_item.items():
        if(keyword in dic_out.keys()):
            outdic[keyword] += keyword_count
        else:
            outdic[keyword] = keyword_count
    return outdic

#for plda
def extract_word_freq(file_folder_path):
    out_folder = 'data/location_wordfreq/'
    jieba.load_userdict("data/user_dict.txt")
    stop_word = []

    with open('data/stop_word.txt', 'r', encoding='utf-8') as sw_f:
        for item in sw_f:
            stop_word.append(item.strip())

    current_keyword = file_folder_path.split('/')[-1]
    file_name_list = os.listdir(file_folder_path)
    temp_list = [file_folder_path + '/' + filename for filename in file_name_list]
    for current_file in temp_list:
        #xxx.txt
        current_city_filename = current_file.split('/')[-1]
        with open(current_file, 'r',encoding='utf-8') as file:
            keyword_out_dic = {}
            weibo_cut_list = []
            line_count = 0
            for temp_line in file:
                weibo_origin = filer.filer(temp_line).replace('/', '')
                weibo_cut = list(jieba.cut(weibo_origin))
                for items in weibo_cut:
                    if (items not in stop_word and len(items.strip()) > 0):
                        weibo_cut_list.append(items)
                line_count += 1
                if(line_count >= 10000):
                    fd = FreqDist(weibo_cut_list)  # nltk库提供的词频统计
                    keyword_out_dic = merege_iter(keyword_out_dic,fd)
                    line_count = 0
                    weibo_cut_list = []

            if(line_count > 0):
                fd = FreqDist(weibo_cut_list)  # nltk库提供的词频统计
                keyword_out_dic = merege_iter(keyword_out_dic, fd)
                line_count = 0
                weibo_cut_list = []

            sort_dict = sorted(keyword_out_dic.items(), key=lambda d: d[1], reverse=True)

            temp_count = 0
            outfile = open(out_folder+current_keyword,'a+',encoding='utf-8')

            for current_tuple in sort_dict:
                temp_count += 1
                outfile.write(str(current_tuple[0]))
                outfile.write(' ')
                outfile.write(str(current_tuple[1]))
                outfile.write(' ')
                if(temp_count >= 50):
                    break
            outfile.write('\n')
            outfile.close()
            # fd.plot(50,cumulative=True)


if __name__=='__main__':
     #lda
     # topic_sta1.keyword_location_lda()


     # 抽取plda所需词频文件
     weibocityfilefolder = '/Volumes/data/chinadream/keyword_location/'
     keyword_folder_name = os.listdir(weibocityfilefolder)
     for current_keyword_name in keyword_folder_name:
         current_keyword_folder = weibocityfilefolder + current_keyword_name
         extract_word_freq(current_keyword_folder)

     #输出结果
     # topic_sta1.lda_city_topic()