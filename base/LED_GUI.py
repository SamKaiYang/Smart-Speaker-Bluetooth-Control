from tkinter import *
from gpiozero import LED
import time


window= Tk()
window.geometry("1000x600")
window.title("ROBO TEST")

led = LED(4) # GPIO 4 output



def on():
    led.on()
def off():
    led.off()
    


B1 = Button(window, text="ON", width=20, bg="yellow", fg="black", command=on)
B1.place(x=150,y=50)

B2 = Button(window, text="OFF", width=20, bg="yellow", fg="black", command=off)
B2.place(x=350,y=50)

window.mainloop()