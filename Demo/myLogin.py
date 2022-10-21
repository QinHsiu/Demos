import tkinter
import tkinter.messagebox
import tkinter.ttk
import re

#初始化窗体
root=tkinter.Tk()

#初始化窗口大小
root["width"]=500
root["height"]=500

#初始化窗口标题
root.title("Login")


#创建文本框初始值/两种初始化方式
varName=tkinter.StringVar(value='')
varPwd=tkinter.StringVar(value='')

#varPwd=tkinter.StringVar(value='')
#设置用户名标签
labelName=tkinter.Label(root,text="user name:",justify=tkinter.RIGHT,width=100)
#设置位置
labelName.place(x=125,y=250,width=100,height=50)
#设置密码标签
labelPwd=tkinter.Label(root,text="user pwd:",justify=tkinter.RIGHT,width=100)
#设置位置
labelPwd.place(x=125,y=300,width=100,height=50)

#设置文本框
entryName=tkinter.Entry(root,width=100,textvariable=varName)
#设置文本框位置
entryName.place(x=225,y=260,width=100,height=25)

entryPwd=tkinter.Entry(root,width=100,textvariable=varPwd)
entryPwd.place(x=225,y=310,width=100,height=25)

username=["QinHsiu","Qxy","Qin"]
userpwd=["123456","1234567","Qxy"]


def Login():
    name=entryName.get()
    pwd=entryPwd.get()
    if (name not in username) or (pwd !=userpwd[username.index(name)]):
        tkinter.messagebox.showerror(title='Error',message='Content error or not exist!')
    else:
        tkinter.messagebox.showinfo(title='OK',message='Welcome!')

#定义操作函数
buttonOk=tkinter.Button(root,text="Login",command=Login)
buttonOk.place(x=50,y=350,width=50,height=20)

def Cancel():
    varName.set('')
    varPwd.set('')

buttonCancel=tkinter.Button(root,text = "Cancel",command = Cancel)
buttonCancel.place(x=250,y=350,width=50,height=20)

def Out():
    if tkinter.messagebox.showinfo(title="Tips",message="Are You sure!"):
        root.destroy()
buttonOut=tkinter.Button(root,text="Out",command=Out)
buttonOut.place(x=150,y=350,width=50,height=20)



def Register():
    # 初始化窗体
    root1 = tkinter.Tk()
    root1["width"] = 300
    root1["height"] = 300
    # 设置用户名标签
    labelName = tkinter.Label(root1, text="user name:", justify=tkinter.RIGHT, width=100)
    # 设置位置
    labelName.place(x=25, y=50, width=100, height=50)
    # 设置密码标签
    labelPwd = tkinter.Label(root1, text="user pwd:", justify=tkinter.RIGHT, width=100)
    # 设置位置
    labelPwd.place(x=25, y=100, width=100, height=50)
    # 设置文本框
    entryName = tkinter.Entry(root1, width=100, textvariable=labelName)
    # 设置文本框位置
    entryName.place(x=125, y=60, width=100, height=25)
    entryPwd = tkinter.Entry(root1, width=100, textvariable=labelPwd)
    entryPwd.place(x=125, y=110, width=100, height=25)

    def Register1():
        name = entryName.get()
        pwd = entryPwd.get()
        if name not in username:
            username.append(name)
            userpwd.append(pwd)
            root1.destroy()
    buttonRegister1= tkinter.Button(root1, text="Register", command=Register1)
    buttonRegister1.place(x=150, y=150, width=50, height=20)


buttonRegister=tkinter.Button(root,text="Register",command=Register)
buttonRegister.place(x=350,y=350,width=50,height=20)



if __name__=="__main__":
    #运行程序
    root.mainloop()
