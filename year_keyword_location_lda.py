# -*- coding: utf-8 -*-
"""
-------------------------------
   Time    : 2019-03-18 15:48
   Author  : diw
   Email   : di.W@hotmail.com
   File    : year_keyword_location_lda.py
   Desc:    # 某年某个中国梦的所有情感(默认)下的 关于市（直辖市的区）级的LDA
-------------------------------
"""
from topic_sta1 import year_keyword_location_lda
import gensim
import pyLDAvis
import pyLDAvis.gensim

keyword_list = ['个人努力', '个体,自由', '中国经济,持续发展', '事业有成', '健康', '出名', '发展,机会', '好工作', '安享晚年', '家庭,幸福', '平等,机会', '成为,富人', '收入,足够', '有房', '父辈,更好', '生活,幸福', '白手起家', '祖国强大']
year_list = [2014,2015,2016]

def ldavis(current_year,current_keyword,mood_list = 'all'):
    output_model_folder = 'data/year_keyword_location_lda/model/' + str(current_year) + '_' + current_keyword + '_' + mood_list

    model_file = output_model_folder + '/' + str(current_year) + '_' + current_keyword + '_' + mood_list + '_lda.model'
    dictionary_file = output_model_folder + '/' + str(current_year) + '_' + current_keyword + '_' + mood_list + '_lda.dict'
    corpus_file = output_model_folder + '/' + str(current_year) + '_' + current_keyword + '_' + mood_list + '_lda.mm'

    dictionary = gensim.corpora.Dictionary.load(dictionary_file)
    corpus = gensim.corpora.MmCorpus(corpus_file)
    lda = gensim.models.ldamodel.LdaModel.load(model_file)

    vis = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.save_html(vis, output_model_folder + '/lda.html')
    return 0

if __name__ == '__main__':
    analyse_keyword = ['平等,机会','祖国强大','个人努力']
    # for current_keyword in analyse_keyword:
    #     for current_year in year_list:
    #         year_keyword_location_lda(current_year,current_keyword)

    ldavis('2014',analyse_keyword[0])