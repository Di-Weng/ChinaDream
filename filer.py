#coding:utf-8
import cn_t_2_s
import re
def remove_at(tweet):
    del_at=r'@.*?\s|@.*?$'
    tweet=re.sub(del_at,'',tweet)
    return tweet
def remove_share(tweet):
    return  re.sub(r'（分享自.*?）','',tweet)
def remove_emoticon(tweet):
    del_emo=r'\[.*?\]'
    return re.sub(del_emo,'',tweet)
def remove_url(tweet):
    url_pattern=r'http://t.cn/\w+'
    tweet=re.sub(url_pattern,'',tweet)
    return tweet
def filer(weibo):
    weibo=cn_t_2_s.zh_simple(weibo)
    weibo=remove_at(weibo)
    weibo=remove_emoticon(weibo)
    weibo=remove_url(weibo)
    weibo=remove_share(weibo)
    return weibo