import tkinter as tk 
import time 
from time import sleep
from tkinter.messagebox import *
#from gpiozero import LED

app = tk.Tk() 
app.geometry('300x200')
app.title("Tkitner Example")

#led = LED(4)  # GPIO 4 output

scaleExample = tk.Scale(app,
                        orient='horizontal',
                        resolution=0.1,
                        from_=0,
                        to=1)
scaleExample.pack()

#顯示現在時間
time_string = time.strftime('%H:%M:%S')
label_text = tk.Label(app, text = time_string).pack()

def get():
    print(scaleExample.get())
    time_step = scaleExample.get() ## 使用scale設定時間值

def eat_medicine_check():
    MsgBox = askquestion("Inform", "Really turn off reminder to take medicine?")
    if MsgBox == 'yes':
        tk.messagebox.showinfo('Welcome','Remind to abort')
        ### 請將吃藥時間提醒歸零
    else:
        tk.messagebox.showinfo('Welcome','Please take medicine in time')
b1=tk.Button(app,text='start',command=eat_medicine_check)
b1.pack()
b2=tk.Button(app,text='get scale value',command=get)
b2.pack()

app.mainloop()
