import tkinter
import tkinter.colorchooser
import tkinter.dialog
import tkinter.ttk
import tkinter.messagebox

mycolor=tkinter.Tk()
mycolor['width']=500
mycolor['height']=500

def choseColor():
    color=tkinter.colorchooser.askcolor()[1]
    color1=tkinter.colorchooser.askcolor()[0]
    #color2=tkinter.colorchooser.askcolor()
    if color:
        tkinter.messagebox.showinfo(title="color",message="choose color is"+color)

button=tkinter.Button(mycolor,text="ColorOpen",justify=tkinter.RIGHT,command=choseColor)
button.place(x=100,y=100,width=100,height=20)


if __name__ == '__main__':
    mycolor.mainloop()