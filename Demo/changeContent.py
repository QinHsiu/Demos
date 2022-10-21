import tkinter
import tkinter.ttk

app=tkinter.Tk()
app['width']=500
app['height']=500
app.title("change")
#设置字符串值
s1 = tkinter.StringVar(value='Open')
s2 = tkinter.StringVar(value="Close")
s3=["Open","Close"]

#用来记录按钮次数
i=0
def onButton():
    #使用全局变量
    global i,button,label
    i+=1
    m=i
    #根据按钮次数动态修改指定值
    if i%2==0:
        s1.set("Close")
        s2.set("Open")
        button["text"]=s1.get()
        label["text"]=s1.get()
    else:
        button["text"]=s2.get()
        label["text"]=s2.get()
        s2.set("Close")
        s1.set("Open")

#创建标签并初始化标签文本
label = tkinter.Label(app,text="Close",justify=tkinter.RIGHT, width=80)
label.place(x=50, y=50, width=50, height=50)
#初始化文本框并初始化
entry=tkinter.Entry(app,width=80,textvariable=s2)
entry.place(x=50,y=100,width=50,height=50)
#初始化按钮并设置初始值
button=tkinter.Button(app,text="Close",command=onButton)
button.place(x=100,y=300,width=50,height=50)

if __name__=="__main__":
    app.mainloop()