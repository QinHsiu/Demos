import tkinter
import tkinter.messagebox
import tkinter.ttk
import re
import random

#初始化窗体
root=tkinter.Tk()

#初始化窗口大小
root["width"]=1000
root["height"]=1000

#初始化窗口标题
root.title("Points24")

# 用来记录用户答对题目数量
count=0

# 用来记录总的题目数量
total=1

# 用来判断是否添加了元素
isnext=True

# 返回四个字符和一个字典
def randNumber(n):
    cards=[str(i) for i in range(2,11)]
    cards.insert(0,'A')
    cards.extend(['J','Q','K'])
    value=[i for i in range(1,14)]
    dic=dict(zip(cards,value))
    tempCards=cards*4
    showvalue=random.sample(tempCards,n)
    return showvalue,dic



# 展示所获得的结果
showvalue,dic=randNumber(4)
#设置用户名标签
labelFirstValue=tkinter.Label(root,text='init value: '+' '.join(showvalue),justify=tkinter.RIGHT,width=100)
#设置位置
labelFirstValue.place(x=150,y=100,width=200,height=50)

#创建文本框初始值/两种初始化方式
varName=tkinter.StringVar(value='')
#设置用户名标签
labelName=tkinter.Label(root,text="input answer:",justify=tkinter.RIGHT,width=100)
#设置位置
labelName.place(x=125,y=200,width=100,height=50)
#设置文本框
entryName=tkinter.Entry(root,width=100,textvariable=varName)
#设置文本框位置
entryName.place(x=250,y=200,width=100,height=25)


def Check():
    global count
    global entryName
    global total
    global isnext
    answer=entryName.get()
    target=False
    v=list(answer)
    for i in range(len(v)):
        if v[i] in ['A','J','K','Q']:
            v[i]=str(dic[v[i]])
    #print(v)
    #print("".join(v))
    if answer=='False':
        t = list(showvalue)
        for i in range(len(t)):
            if t[i] in ['A', 'J', 'K', 'Q']:
                t[i] = str(dic[t[i]])
        trueValue = [int(i) for i in t]
        if twentyfour(trueValue)==False:
            count+=1
            target=True
    else:
        if eval(''.join(v))==24:
            count+=1
            target=True

    if target==False:
        tkinter.messagebox.showerror(title='Error',message='The answer is error!')
    else:
        tkinter.messagebox.showinfo(title='OK',message='Congratulations!')
        if not isnext:
            count-=1
    isnext=False



#定义操作函数
buttonOk=tkinter.Button(root,text="Check",command=Check)
buttonOk.place(x=50,y=350,width=50,height=20)


def Cancel():
    varName.set('')

buttonCancel=tkinter.Button(root,text = "Reset",command = Cancel)
buttonCancel.place(x=150,y=350,width=50,height=20)

# 下一题
def Next():
    global showvalue
    global varName
    global entryName
    global isnext
    isnext=True
    showvalue,dic=randNumber(4)
    # 设置用户名标签
    labelFirstValue = tkinter.Label(root, text='init value: ' + ' '.join(showvalue), justify=tkinter.RIGHT, width=100)
    # 设置位置
    labelFirstValue.place(x=150, y=100, width=200, height=50)

    global total
    total+=1
    # 创建文本框初始值/两种初始化方式
    varName = tkinter.StringVar(value='')
    # 设置用户名标签
    labelName = tkinter.Label(root, text="input answer:", justify=tkinter.RIGHT, width=100)
    # 设置位置
    labelName.place(x=125, y=200, width=100, height=50)
    # 设置文本框
    entryName = tkinter.Entry(root, width=100, textvariable=varName)
    # 设置文本框位置
    entryName.place(x=250, y=200, width=100, height=25)


buttonNext=tkinter.Button(root,text="Next",command=Next)
buttonNext.place(x=350,y=350,width=50,height=20)


import itertools
def twentyfour(truevalue):
    for ops in itertools.product('+-*/',repeat=3):
        bds1 = '({0}{4}{1}){5}({2}{6}{3})'.format(*truevalue, *ops)  # (a+b)*(c-d)
        bds2 = '(({0}{4}{1}){5}{2}){6}{3}'.format(*truevalue, *ops)  # (a+b)*c-d
        bds3 = '{0}{4}({1}{5}({2}{6}{3}))'.format(*truevalue, *ops)  # a/(b-(c/d))
        for bds in [bds1, bds2, bds3]:  # 遍历
            try:
                if abs(eval(bds) - 24.0) < 1e-10:  # eval函数
                    return bds
            except ZeroDivisionError:  # 零除错误！
                continue
    return False


def Show():
    answer=showvalue
    target=False
    v=list(answer)
    #print(v)
    for i in range(len(v)):
        if v[i] in ['A','J','K','Q']:
            v[i]=str(dic[v[i]])
    #print(list(dic.keys()),v)
    trueValue=[int(i) for i in v]
    # print(trueValue)
    if twentyfour(trueValue) !=False:
        answer=twentyfour(trueValue)
        tkinter.messagebox.showinfo(title='OK', message=answer)
    else:
        tkinter.messagebox.showerror(title='Error', message='No answer!')


buttonOut=tkinter.Button(root,text="Show",command=Show)
buttonOut.place(x=450,y=350,width=50,height=20)





def Score():
    global total
    global count
    tkinter.messagebox.showinfo(title='Accuracy rate', message="total %d , accuracy %d  accuracy rate %.2f"%(total,count,count/total))
buttonScore=tkinter.Button(root,text="Score",command=Score)
buttonScore.place(x=550,y=350,width=50,height=20)

def Out():
    if tkinter.messagebox.showinfo(title="Tips",message="Are You sure!"):
        root.destroy()
buttonOut=tkinter.Button(root,text="Out",command=Out)
buttonOut.place(x=650,y=350,width=50,height=20)


if __name__=="__main__":
    #运行程序
    #print(random.sample([i for i in range(13)],4))
    root.mainloop()
