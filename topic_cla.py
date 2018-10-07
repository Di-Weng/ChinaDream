#coding:utf-8
'''
1：生成类别标号文件
2：生成训练集与测试集
'''
import os
import filer
import jieba

#相对本py文件的路径
word_dict_filename='word_topic_probability'
category_filename='category_label.txt'
category_list=[]
pre_probability_dict={}
pre_category_probability_dict={}
training_word_set=set()

def get_all_word(training_dir):
    all_word_list=[]
    for category in category_list:
        f=open('%s/%s' % (training_dir,category),'r',encoding = 'utf-8')
        for line in f:
            word_list=line.strip().split('|')
            all_word_list+=word_list
        f.close()
    return set(all_word_list)
def get_pre_category_probability_dict():
    global pre_category_probability_dict
    f=open(word_dict_filename, 'r', encoding = 'utf-8')
    for line in f:
        line_arr=line.strip().split('\t')
        pre_category_probability_dict[line_arr[0]]=[float(value) for value in line_arr[1:]]
def get_category(training_dir):
    category_list=os.listdir(training_dir)
    num=0
    category_dict={}
    for category in category_list:
        category_dict[category]=num
        num+=1
    sorted_category_list=sorted(category_dict.items(),key=lambda d:d[1])
    f_out=open(category_filename,'w')
    for (category,value) in sorted_category_list:
        f_out.write('%s:%s\n' % (category,value))
    f_out.close()
    return category_dict
def get_category_list():
    global category_list
    print(category_filename)
    f=open(category_filename,'r',encoding = 'utf-8')
    for line in f:
        category_list.append(line.strip().split(':')[0])
    f.close()
def get_pre_probability():
    global pre_probability_dict
    for category in category_list:
        pre_probability_dict[category]=1.0/len(category_list)
def train(training_dir):
    all_word_dict=dict([(word,[]) for word in training_word_set])
    for category in category_list:
        word_dict={}
        all_num=0
        f=open('%s/%s' % (training_dir,category),'r',encoding = 'utf-8')
        for line in f:
            word_list=line.strip().split('|')
            all_num+=len(word_list)
            for word in set(word_list):
                try:
                    word_dict[word]+=word_list.count(word)
                except KeyError:
                    word_dict[word]=word_list.count(word)
        f.close()
        for word in all_word_dict:
            if word in word_dict:
                n_word=word_dict[word]
            else:
                n_word=0
            all_word_dict[word].append(str((n_word+1)/float(all_num+len(all_word_dict))))
    f_out=open(word_dict_filename,'w')
    for word in all_word_dict:
        f_out.write('%s\t%s\n' % (word,'\t'.join(all_word_dict[word])))
    f_out.close()
def predict(weibo):
    # print(weibo)
    weibo=filer.filer(weibo)
    word_list=[word for word in jieba.cut(weibo)]
    if len(word_list)<5:
        return -1

    result_list=list(pre_probability_dict.values())
    for word in word_list:
        if word in pre_category_probability_dict:
            for i in range(0,len(category_list)):
                result_list[i]*=pre_category_probability_dict[word][i]
    max_category=0
    for i in range(0,len(category_list)):
        if result_list[i]>result_list[max_category]:
            max_category=i
    return category_list[max_category]
def test(testing_dir):
    correct_num=0
    all_num=0
    for category in category_list:
        f=open('%s/%s' % (testing_dir,category),'r',encoding = 'utf-8')
        for line in f:
            if predict(line.strip().split('|'))==category:
                correct_num+=1
            all_num+=1
            if all_num%1000==0:
                print(all_num)
    return correct_num/float(all_num)

def extract():
    correct_num=0
    f=open('/mnt2/fanrui/technology/id.2013101112/id.2013101112_use.txt')
    f_out=open('/mnt2/fanrui/technology/id.2013101112/科技.txt','w')
    for line in f:
        if predict(line.strip().split('|'))=='科技':
            f_out.write(line)

get_category_list() #类别列表
print(category_list)
#    training_word_set=get_all_word('training')
get_pre_probability()#先验
get_pre_category_probability_dict()#类先验
# print(pre_category_probability_dict)
'''
if __name__=='__main__':
#训练
    global training_word_set
    get_category_list() #类别列表
    training_word_set=get_all_word('training')
    train('training')
#测试
    global training_word_set
    get_category_list() #类别列表
#    training_word_set=get_all_word('training')
    get_pre_probability()#先验
    get_pre_category_probability_dict()#类先验
#    test('testing')
    extract()
'''
