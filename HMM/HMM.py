import numpy as np
import pandas as pd
import jieba
import re
import os

def pre_process(filename):
    with open(filename,'r',encoding="utf-8") as f:
        data=f.readlines() # 读取所有数据
    total_data=[]
    err=[]
    # 将数据按照词性进行切分
    for line in data[1:]: # 去掉第一行的标题
        line_data=[]
        temp=line.split('\t\t')
        index,content=temp[0],temp[1] # 获取索引和内容
        # content=re.findall('\[[\u4e00-\u9fa5]\]',content)
        content=re.sub(' \[[\u4e00-\u9fa5]\] ','你',content) # 替换操作
        content=content.strip('\n') # 删除换行符
        for v in content.split(' '):
            # print("v: ",v,index,len(v))
            if len(v)<2:
                continue
            else:
                try:
                    t_a,t_b=v.split('/') # 词语与标注
                    if t_b=='' or t_b==' ':
                        continue
                    line_data.append((t_a,t_b)) # 将有用的词与词性标注放入数据
                except:
                    err.append([index,content])
                    continue
        total_data.append(line_data)
    # print(len(err),err)
    # print(len(total_data),total_data[0])
    return total_data

# 数据集分析
def data_analysis(data,a_train_data,a_test_data,train_data,test_data,total_data):
    data_t=[total_data,train_data,test_data]
    T_s=[]
    W_s=[]
    for d_ in data_t:
        words=[]
        tags=[]
        for w_ in d_:
            words.append(w_[0])
            tags.append(w_[1])
        words=list(set(words))
        tags=list(set(tags))
        W=len(words) # 词汇量
        T=len(tags) # 词性数目
        T_s.append(T)
        W_s.append(W)
    print(pd.DataFrame({"DataName":['total_data','train_data','test_data'],"DataLength":[len(data),len(a_train_data),len(a_test_data)],"NumTag":T_s,"NumWord":W_s},index=[0,1,2]))



def train_test_split(data,mode=0,portion=None):
    """
    :param data: original data
    :param mode: 选择训练集与测试集方式（1: 留一法；2: 交叉验证；3: 自己设置比例）
    :param portion: 训练集的比例
    """
    l=len(data)
    if mode==0: # 采用留一法划分训练与测试集
        train_data=data[:(l//10)*9]
        test_data=data[(l//10)*9:]
    else: #采用特定的比例划分训练集与测试集
        train_data=data[:int(l*portion)]
        test_data=data[int(l*portion):]
    assert len(train_data)+len(test_data)==len(data)
    train_datas=[]
    test_datas=[]
    total_data=[]
    for tr_ in train_data:
        train_datas.extend(tr_)
        total_data.extend(tr_)
    for te_ in test_data:
        test_datas.extend(te_)
        total_data.extend(te_)
    return train_data,test_data,np.array(train_datas,dtype=str),np.array(test_datas,dtype=str),np.array(total_data,dtype=str)



class HMM:
    def __init__(self,train_data,test_data,total_data,smooth):
        """
        :param train_data: train data
        :param test_data: test data
        """
        self.train_data=train_data
        self.test_data=test_data
        self.total_data=total_data
        self.smooth=smooth


    # 获取所有所用词与词性数目
    def get_data(self,data):
        words=[]
        tags=[]
        for w_ in data:
            words.append(w_[0])
            tags.append(w_[1])
        words=list(set(words))
        tags=list(set(tags))
        W=len(words) # 词汇量
        T=len(tags) # 词性数目
        # print(pd.DataFrame({"DataName":'corpus_你_20211101164534',"DataLength":33075,"NumTag":T,"NumWord":W},index=[0]))
        return T,W,words,tags

    def fit(self):
        T, W, words, tags = self.get_data(self.total_data)
        self.word2id = {words[i]: i for i in range(W)} # 单词：id映射
        self.tag2id = {tags[i]: i for i in range(T)} # 词性：id映射
        self.id2tag = {i: tags[i] for i in range(T)} # id：词性映射

        """HMM训练"""
        self.emit_p = np.zeros((T, W)) + self.smooth  # emission_probability
        self.start_p = np.zeros(T) + self.smooth  # start_probability，Π
        self.trans_p = np.zeros((T, T)) + self.smooth  # transition_probability

        pre_tag='start'
        for word, tag in self.train_data:
            wid, tid = self.word2id[word], self.tag2id[tag]
            self.emit_p[tid][wid] += 1
            if pre_tag=='start':
                self.start_p[tid]+=1
            else:
                self.trans_p[self.tag2id[pre_tag]][tid] += 1
            pre_tag='start' if tag=='w' else tag
        # 频数 --> 概率对数
        self.start_p = np.log(self.start_p / sum(self.start_p))
        for i in range(T):
            self.emit_p[i] = np.log(self.emit_p[i] / sum(self.emit_p[i]))
            self.trans_p[i] = np.log(self.trans_p[i] / sum(self.trans_p[i]))


    def transform(self,sentence=None):
        T, W, words, tags = self.get_data(self.total_data)

        err=0.0

        if sentence==None:
            for word,tag in self.test_data:
                # print(word,tag)
                # print(self.word2id[word])

                """维特比算法"""
                obs = [self.word2id[word]]  # 观测序列
                le = len(obs)  # 序列长度

                # 动态规划矩阵
                dp = np.zeros((le, T))  # 记录节点最大概率对数
                path = np.zeros((le, T), dtype=int)  # 记录上个转移节点

                for j in range(T):
                    dp[0][j] = self.start_p[j] + self.emit_p[j][obs[0]]

                for i in range(1, le):
                    for j in range(T):
                        dp[i][j], path[i][j] = max(
                            (dp[i - 1][k] + self.trans_p[k][j] + self.emit_p[j][obs[i]], k)
                            for k in range(T))
                # 隐序列
                states = [np.argmax(dp[le - 1])]
                # 从后到前的循环来依次求出每个单词的词性
                for i in range(le - 2, -1, -1):
                    states.insert(0, path[i + 1][states[0]])

                if self.id2tag[states[0]]!=tag:
                    err+=1
            print("Test Error: {:.2f}".format(err/len(self.test_data)))
        else:
            # word_s=jieba.lcut(sentence,cut_all=False)
            word_s=sentence.split(' ')
            # print(word_s)
            try:
                obs = [self.word2id[w] for w in word_s]  # 观测序列
                le = len(obs)  # 序列长度
            except:
                print("The key don't exist!")

            # 动态规划矩阵
            dp = np.zeros((le, T))  # 记录节点最大概率对数
            path = np.zeros((le, T), dtype=int)  # 记录上个转移节点

            for j in range(T):
                dp[0][j] = self.start_p[j] + self.emit_p[j][obs[0]]

            for i in range(1, le):
                for j in range(T):
                    dp[i][j], path[i][j] = max(
                        (dp[i - 1][k] + self.trans_p[k][j] + self.emit_p[j][obs[i]], k)
                        for k in range(T))

            # 隐序列
            states = [np.argmax(dp[le - 1])]

            # 从后到前的循环来依次求出每个单词的词性
            for i in range(le - 2, -1, -1):
                states.insert(0, path[i + 1][states[0]])

            # 打印
            st=''
            for word, tid in zip(word_s, states):
                # print(word, self.id2tag[tid])
                st=st+word+'/'+self.id2tag[tid]+' '
            print("加入词性分析之后：",st)




if __name__ == '__main__':
    # 获取本地数据文件
    filenames=os.listdir(os.getcwd())
    filename=os.getcwd()+"//"+filenames[[i for i in range(len(filenames)) if filenames[i][-4:]==".txt"][0]]
    data=pre_process(filename)
    # 训练集与测试集
    a_train_data,a_test_data,train_data,test_data,total_data=train_test_split(data)
    # 分析数据集
    data_analysis(data, a_train_data, a_test_data,train_data,test_data,total_data)
    # 模型初始化
    myHMM=HMM(train_data,test_data,total_data,1e-8)
    # 开始训练
    myHMM.fit()
    # 进行测试
    myHMM.transform()
    s='爷爷 三 月 里 买 了 四 只 小猪 ， 说 你 底 桑树 太 荒 了 。'
    print("原始句子： ",s)
    myHMM.transform(s)











