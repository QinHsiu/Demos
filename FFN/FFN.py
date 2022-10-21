import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import argparse
import time

from utils import *
from torch.optim import Adam
from tqdm import tqdm

# 构造类
class FFN(nn.Module):
    def __init__(self,args):
        super(FFN,self).__init__()
        # 层的数目
        self.l_num=args.l_num
        # 输入层的神经元个数
        self.i_num=args.i_num
        # 隐藏层的神经元个数，数据类型为list
        self.h_num=eval(args.h_num)
        # 输出层神经元个数
        self.o_num=args.o_num
        # 激活函数
        self.act_f=ACT2FN[args.act_function]
        # 模型参数
        self.Linears=self.create_ffn()
        # 参数初始化
        self.apply(self._init_weights)
    # 构建模型框架
    def create_ffn(self):
        temp=nn.ModuleList()
        if not isinstance(self.h_num,list):
            raise ValueError("the type of hidden layer nums must be a list!")
        temp.append(nn.Linear(self.i_num,self.h_num[0])) # 输入层
        for h in range(len(self.h_num)-1):
            temp.append(nn.Linear(self.h_num[h],self.h_num[h+1]))
        temp.append(nn.Linear(self.h_num[-1],self.o_num))
        return temp

    # 权重，偏执初始化（参数初始化）
    def _init_weights(self,m):
        if isinstance(m,(nn.Linear,nn.Embedding)):
            m.weight.data.normal_(mean=0.0,std=1e-2)
        elif isinstance(m,nn.BatchNorm1d):
            pass
        elif isinstance(m,LayerNorm):
            m.bias.data.zero_()
            m.weight.data.fill_(1.0)
        if isinstance(m,nn.Linear) and m.bias is not None:
            m.bias.data.zero_()
    # 前向传播
    def forward(self,data):
        out_put=data
        for i_ in range(len(self.Linears)-1):
            out_put=self.Linears[i_](out_put)
            out_put=self.act_f(out_put) # 激活

        out_put=self.Linears[-1](out_put)
        # out_put=nn.Softmax()(out_put)
        return out_put





# 测试模型
def test(data,label,FFN,args):
    loss_f=get_loss(args)
    data_train=torch.tensor(data[0])
    label_train=torch.tensor(label[0],dtype=torch.long)
    best_evel_result=[]
    # 优化器
    betas = (args.adam_beta1, args.adam_beta2)
    optim = Adam(FFN.parameters(), lr = args.lr, betas = betas, weight_decay = args.weight_decay)
    train_es=[]
    train_ls=[]
    for b_ in range(math.ceil(len(data_train) / args.batch_size)):
        train_e = data_train[b_ * args.batch_size:(b_ + 1) * args.batch_size, :]
        train_l=label_train[b_*args.batch_size:(b_+1)*args.batch_size]
        train_es.append(train_e)
        train_ls.append(train_l)

    data_eval = [torch.tensor(data[1])]
    label_eval = torch.tensor(label[1], dtype=torch.long)


    data_test = [torch.tensor(data[1])]
    label_test = torch.tensor(label[1], dtype=torch.long)

    train_losses=[]
    test_losses=[]

    es=0
    if args.do_eval==True:
        model_path=args.model_path
        if os.path.exists(model_path):
            FFN.load_state_dict(torch.load(model_path))
            FFN.eval()
            print("load {} the best model for testing!".format(args.model_path))
            for b_, test_e in tqdm(enumerate(data_test), total=len(data_test),
                                   desc=set_color(f"Testing ", 'pink'), ):
                output = FFN(test_e)
                # print(b_,data_train.shape,train_e.shape)
                loss = loss_f(output, label_test)
            time.sleep(0.5)
            print("test loss:{:.4f}".format(loss))
        else:
            raise ValueError("no model for testing!")

    else:
        for e_ in range(args.epoch):
            FFN.train()
            for b_,train_e in tqdm(enumerate(train_es),total=len(train_es),desc=set_color(f"Training {e_:>5}", 'pink'),):
                output=FFN(train_e)
                # print(b_,data_train.shape,train_e.shape)
                if b_==0:
                    loss=loss_f(output,train_ls[b_])
                else:
                    loss+= loss_f(output,train_ls[b_])

            if torch.isnan(loss):
                raise ValueError("loss is nan")

            train_losses.append(loss)

            optim.zero_grad()
            loss.backward()
            optim.step()
            # time.sleep(0.5)
            print("epoch: {0} training loss:{1:.4f}".format(e_,loss))
            # time.sleep(0.5)

            FFN.eval()
            for b_,eval_e in tqdm(enumerate(data_eval),total=len(data_eval),desc=set_color(f"Valid {e_:>5}", 'pink'),):
                output=FFN(eval_e)

                # print(b_,data_train.shape,train_e.shape)
                loss=loss_f(output,label_eval)
            test_losses.append(loss)
            # time.sleep(0.5)

            if len(best_evel_result)==0:
                best_evel_result.append(loss)
                print("the valid loss is descending:{:.4f},save the best model".format(loss))
                torch.save(FFN.cpu().state_dict(), args.model_path)
            elif best_evel_result[0]<loss:
                print("early stop :{}".format(es))
                es+=1
            else:
                print("the valid loss is descending:{:.4f},save the best model".format(loss))
                torch.save(FFN.cpu().state_dict(), args.model_path)

            # 判断早停
            if es==args.early_stop:
                break
        # 绘制loss函数的图像
        if args.batch_size==256:
            draw_plot(torch.tensor([train_losses,test_losses]).detach().cpu().numpy().tolist())

        #测试集效果
        FFN.load_state_dict(torch.load(args.model_path))
        for b_, test_e in tqdm(enumerate(data_test), total=len(data_test), desc=set_color(f"Testing ", 'pink'), ):
            output = FFN(test_e)

            # print(b_,data_train.shape,train_e.shape)
            loss = loss_f(output, label_test)
        print("test loss:{:.4f}".format(loss.detach().cpu().numpy().tolist()))
        return loss










# 相关参数初始化
if __name__ == '__main__':
    random.seed(2022)
    parser=argparse.ArgumentParser()
    # 模型参数
    parser.add_argument("--l_num",default=5,type=int,help="the layers of FFN")
    parser.add_argument("--i_num",default=3,type=int,help="the neural nums of input layer")
    parser.add_argument("--h_num", default='[4,5,4]', type=str, help="the neural nums of hidden layer")
    parser.add_argument("--o_num", default=2, type=int, help="the neural nums of output layer")
    parser.add_argument("--act_function",default="relu",type=str,help="activate function")
    parser.add_argument("--dropout_rate",default=0,type=int,help="dropout rate")

    # 数据集相关参数
    parser.add_argument("--split_ratio", default='[0.7,0.2,0.1]', type=str, help="dropout rate")
    parser.add_argument("--data_length", type=int, default=10000, help="total data length")
    parser.add_argument("--distribution", type=str, default="Binomial", help="label distribution")
    parser.add_argument("--data_path", type=str, default="data.txt", help="data path")

    # 训练和验证部分
    parser.add_argument("--loss_function", default="CrossEntryLoss", type=str, help="loss function")
    parser.add_argument("--epoch", default=50, type=int, help="train epoch")
    parser.add_argument("--early_stop", default=10, type=int, help="early stop")
    parser.add_argument("--batch_size", default=256, type=int, help="batch_size")
    parser.add_argument("--weight_decay", type=float, default=0.0, help="weight_decay of adam")
    parser.add_argument("--adam_beta1", type=float, default=0.9, help="adam first beta value")
    parser.add_argument("--adam_beta2", type=float, default=0.999, help="adam second beta value")
    parser.add_argument("--lr", type=float, default=0.001, help="learning rate of adam")

    # 其他
    parser.add_argument("--do_eval", action="store_true", help="do eval")
    parser.add_argument("--model_path", type=str, default="model.pkl", help="best model path")
    args=parser.parse_args()

    # 打印参数
    show_args_info(args)

    # 创建数据集
    data,label=get_data(args)
    # 划分数据集
    train_data,valid_data,test_data=data_split(data,eval(args.split_ratio))
    train_label,valid_label,test_label=data_split(label,eval(args.split_ratio))

    data=[train_data,valid_data,test_data]
    label=[train_label,valid_label,test_label]

    # 数据统计
    static(data,label)

    # 训练模型
    myFFN = FFN(args)

    batch_results=[]
    batch_sizes=[64,128,256,512]
    for batch_size in batch_sizes:
        args.batch_size=batch_size
        r=test(data,label,myFFN,args)
        batch_results.append(r.detach().numpy().tolist())
    draw_plot_([batch_sizes,batch_results])








