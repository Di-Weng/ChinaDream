#coding:utf-8
import topic_cla
import chardet   #需要导入这个模块，检测编码格式
s = input('input:')
while s!='#':
    print (topic_cla.predict(s))
    s= input('input:')
