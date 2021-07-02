import tkinter as tk 
import threading
from time import sleep
from gpiozero import LED , PWMLED

stop_flag = True # initial

app = tk.Tk() 
app.geometry('300x200')
app.title("Tkitner Example")

led_pwm = PWMLED(4)  # GPIO 4 output

scaleExample = tk.Scale(app,
                        orient='horizontal',
                        resolution=0.1,
                        from_=0,
                        to=1)
scaleExample.pack()

def job():
    global stop_flag
    while(1):
        if stop_flag == False:
            led_pwm.value = scaleExample.get()  
            sleep(1)
        else:
            led_pwm.value = 0
            sleep(1)

t = threading.Thread(target= job)
t.start()

def start():
    global stop_flag
    stop_flag = False
    print(stop_flag)

def stop():
    global stop_flag
    stop_flag = True
    print(stop_flag)


b1=tk.Button(app,text='start',command=start)
b1.pack()

b3=tk.Button(app,text='stop',command=stop)
b3.pack()
app.mainloop()

t.join()

print("Done")
