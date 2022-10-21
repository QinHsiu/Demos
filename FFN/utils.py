from numpy.random import binomial # 伯努利分布
from numpy.random import poisson # 泊松分布
from numpy.random import normal # 正态分布
import random
import torch.nn as nn
import torch
import math
import torch.nn.functional as F
import os
import numpy as np
import pandas as pd

def set_color(log, color, highlight=True):
    color_set = ['black', 'red', 'green', 'yellow', 'blue', 'pink', 'cyan', 'white']
    try:
        index = color_set.index(color)
    except:
        index = len(color_set) - 1
    prev_log = '\033['
    if highlight:
        prev_log += '1;3'
    else:
        prev_log += '0;3'
    prev_log += str(index) + 'm'
    return prev_log + log + '\033[0m'

def gelu(x):
    return x * 0.5 * (1.0 + torch.erf(x / math.sqrt(2.0)))

def swish(x):
    return x * torch.sigmoid(x)


# 激活函数
ACT2FN = {"gelu": gelu, "relu": F.relu, "swish": swish}

# 打印参数信息
def show_args_info(args):
    print(f"--------------------Configure Info:------------")
    for arg in vars(args):
        print(f"{arg:<30} : {getattr(args, arg):>35}")

# 创建数据集
def create_data(data_length=10000,distribution="Binomial"):
    """
    :param feature_num:特征数目
    :param data_length:数据的长度
    :param distribution: 真实标签服从某项分布
    :return: 创建好的数据集
    """
    data=[[] for _ in range(data_length)]
    f_1=[round(i-data_length+i/(i+1),2) for i in range(data_length)]
    f_2=[round(i%data_length+i/(i+1),2) for i in range(data_length)]
    f_3=[round(i/data_length+i/(i+1),2) for i in range(data_length)]
    random.shuffle(f_1)
    random.shuffle(f_2)
    random.shuffle(f_3)
    for i_ in range(data_length):
        data[i_].append(f_1[i_])
        data[i_].append(f_2[i_])
        data[i_].append(f_3[i_])
    distributions=["Norm","Poisson","Binomial"]
    if distribution not in distributions:
        raise ValueError("distribution must in distributions")
    if distribution=="Norm":
        # 均值为5，方差为1（标签为小数）
        label=normal(5,1,data_length)
    elif distribution=='Poisson':
        # 出现概率为0.5，（标签为整数）
        label=poisson(0.5,data_length)
    else:
        # 标签取值为[0,1]，类别所占概率为0.2（标签为整数）
        label=binomial(1,0.2,data_length)
    return data,label

# 获取并保存数据
def get_data(args):
    path=args.data_path
    if os.path.exists(path):
        data=[]
        label=[]
        with open(path,"r+") as fr:
            data_=fr.readlines()
        for d_ in data_:
            line=list(map(eval,d_.split(' ')))
            data.append(line[:-1])
            label.append(line[-1])
    else:
        data,label=create_data(args.data_length,args.distribution)
        with open(path,"w+") as fw:
            for d_,l in zip(data,label):
                fw.write(' '.join(list(map(str,d_)))+" "+str(l)+"\n")
    return data,label

# 统计数据集情况
def static(data_total,label_total):
    data=pd.DataFrame()
    # data.columns=["train","valid","test"]
    train_data=data_total[0]
    train_label=label_total[0]

    valid_data=data_total[1]
    valid_label=label_total[1]

    test_data=data_total[2]
    test_label=label_total[2]


    data["train"]=[np.sum(np.array(train_label)==0),np.sum(np.array(train_label)==1)]
    data["valid"]=[np.sum(np.array(valid_label)==0),np.sum(np.array(valid_label)==1)]
    data["test"]=[np.sum(np.array(test_label)==0),np.sum(np.array(test_label)==1)]

    print(data)
















# 数据切分
def data_split(data,ratio):
    return data[:int(len(data)*ratio[0])],data[int(len(data)*ratio[0]):int(len(data)*(ratio[1]+ratio[0]))],data[int(len(data)*(ratio[1]+ratio[0])):]


# 获取loss函数
def get_loss(args):
    loss_f=args.loss_function
    if loss_f not in ["MSE","CrossEntryLoss"]:
        raise ValueError("loss function error")
    if loss_f=="MSE":
        loss_f=nn.MSELoss()
    else:
        loss_f=nn.CrossEntropyLoss()
    return loss_f


# 绘制图像
import matplotlib.pyplot as plt
import pandas as pd
def draw_scatter(data):
    data=pd.DataFrame(data)
    data.columns=['f1','f2','f3','label']
    ax=plt.Figure()
    plt.scatter(data[data["label"]>0].loc[:,"f1"],data[data["label"]>0].loc[:,"f2"],color="r")
    plt.scatter(data[data["label"]==0].loc[:,"f1"],data[data["label"]==0].loc[:, "f2"], color="b")
    plt.show()

def draw_plot(data):
    fig=plt.Figure()
    plt.plot(range(1,len(data[0])+1),data[0],c="r",marker="*",label="train_loss")
    plt.plot(range(1,len(data[1])+1),data[1],c="b",marker="o",label="valid_loss")
    plt.xlabel("epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.savefig("train_valid.png")
    plt.show()

def draw_plot_(data):
    fig=plt.Figure()
    plt.plot(data[0],data[1],c="b",marker="o",label="test_loss")
    plt.xlabel("batch_size")
    plt.ylabel("Test Loss")
    plt.legend()
    plt.savefig("test_batch_size.png")
    plt.show()



# 层标准化
class LayerNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-12):
        """Construct a layernorm module in the TF style (epsilon inside the square root).
        """
        super(LayerNorm, self).__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.bias = nn.Parameter(torch.zeros(hidden_size))
        self.variance_epsilon = eps

    def forward(self, x):
        u = x.mean(-1, keepdim=True)
        s = (x - u).pow(2).mean(-1, keepdim=True)
        x = (x - u) / torch.sqrt(s + self.variance_epsilon)
        return self.weight * x + self.bias