import tkinter as tk
from time import sleep
from gpiozero import LED , PWMLED
app = tk.Tk() 
app.geometry('300x200')
app.title("Tkitner Scale Example")


led = LED(3) # GPIO 3 output
led_pwm = PWMLED(4)  # GPIO 4 output

scaleExample = tk.Scale(app,
                        orient='horizontal',
                        resolution=0.1,
                        from_=0,
                        to=1)
scaleExample.pack()
                        
def get():
    led.value = scaleExample.get()  
    sleep(1)
    #print(scaleExample.get())
def bright():
    led.on()
    sleep(1)
    led.off()
    sleep(1)
def stop():
    led.off()


b1=tk.Button(app,text='Get',command=get)
b1.pack()

b2=tk.Button(app,text='bright',command=bright)
b2.pack()


b3=tk.Button(app,text='bright stop',command=stop)
b3.pack()

app.mainloop()
