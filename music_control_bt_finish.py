#coding=utf-8  
import uuid
from bluetooth import *
import RPi.GPIO as GPIO,time,pygame,threading,os,json  
from gpiozero import LED, Button
import unicodedata
#GPIO setup  
pinList= [27,22,2,3,17] # 注意!! 請勿設定GPIO(4)會衝突
# Pin2use [volumeup,volumedown,play/pause,next,previous] 
GPIO.setmode(GPIO.BCM)    # 設定BCM編號規則 GPIO(?)
pinVolume = pinList[0:2]   # 設定音量大小pin
GPIO.setup(pinList,GPIO.IN)   # 設定pin為輸入腳
for pinSingle in pinList:   
    GPIO.add_event_detect(pinSingle, GPIO.RISING)  
pinPlay = pinList[2]  # 播放/暫停
pinNext = pinList[3]  # 下一首
pinPrev = pinList[4]  # 上一首
#Default volume value(0.0~1.0)  # 音量調整範圍
volume = 0.50000000  #initial value 
statelist = [0,0]  

server_socket=BluetoothSocket(RFCOMM)
server_socket.bind(("", PORT_ANY))
server_socket.listen(1)
port = server_socket.getsockname()[1]
service_id = str(uuid.uuid4())

advertise_service(server_socket, "Music_Server",
                  service_id = service_id,
                  service_classes = [service_id, SERIAL_PORT_CLASS],
                  profiles = [SERIAL_PORT_PROFILE])

data = None
  
#Music Playing  
with open('index.list','r') as index:  
    filelist = json.loads(index.read())  
    print(filelist)  
lens = len(filelist)  
filePlaying = 0  
pygame.mixer.init()  
track = pygame.mixer.music.load(filelist[filePlaying])  #歌曲讀取
pygame.mixer.music.set_volume(volume)  #音量預設
pygame.mixer.music.play()  #音樂播放
pygame.mixer.music.pause() 
pause=0  
####   main function  ####
# 播放狀態
def playpause():  
    global data, pause  #全域變數
    while True:  
        if data == "pause":  
            data = " "
            print('pause music')  
            pygame.mixer.music.pause()  
            pause=1  
        elif data == "resume":  
            data = " "
            print('resume music')  
            pygame.mixer.music.unpause()  
            pause=0  
        # print('command: {}'.format(data))
        
        time.sleep(0.2)  
# 音量調整功能
def volume():  
        global data, volume   #全域變數
        volume = 0.5  
        while True:  
            if data == "up":   #音量調大觸發事件偵測
                data = " "
                print('volume up')  
                volume = volume + 0.1  
                if volume > 1.0:  
                    volume = 1.0  
                print('volume value:',volume)  
                pygame.mixer.music.set_volume(volume) 
            if data == "down":  #音量調小觸發事件偵測
                data = " "
                print('volume down')  
                volume = volume - 0.1  
                if volume < 0.0:  
                    volume = 0.0  
                print('volume value:',str(round(volume*10)))  #round浮點數的四捨五入值
                pygame.mixer.music.set_volume(volume)  
            
            time.sleep(0.2) 
  
# 音量調整功能
def volume_scale():  
        global data, volume   #全域變數
        volume = 0.5  
        while True:
            if data != None:
                try:
                    vol = float(data)
                    data = " "
                    print(vol)
                    volume = vol/100
                    print('volume value:',str(volume*10)) 
                    pygame.mixer.music.set_volume(volume)
                except ValueError:
                    pass
              
                        
            
            time.sleep(0.2) 
  
#  歌曲切換功能
def switch():  
    global data, filePlaying,track,pause  #全域變數
    while True:  
        
        filePlayingchk = filePlaying  
        if pygame.mixer.music.get_busy() == 0 :  # 判斷是否在播放音樂,本功能為歌曲播放完至下首
            filePlaying = filePlaying + 1  
        else:  
            if data == "next":  #下一首觸發事件偵測
                data = " "
                filePlaying = filePlaying + 1  

            if data == "prev":  #上一首大觸發事件偵測
                data = " "
                filePlaying = filePlaying - 1  

        if filePlaying < 0:  
            filePlaying = lens -1  
        elif filePlaying > lens -1:  
            filePlaying = 0  
        if filePlayingchk != filePlaying :  
            track = pygame.mixer.music.load(filelist[filePlaying])  
            pygame.mixer.music.play()  # 播放
            pause = 0  
            print(filePlaying + 1,filelist[filePlaying])  #輸出歌名

        time.sleep(0.2)  

#  歌曲指定功能
def specify():  
    global data, filePlaying,track,pause  #全域變數
    while True:
        if data != None:
            try:
                
                data_str = data.split(' ')
                if data_str[0] == "@": 
                    data = " "
                    file = int(data_str[1]) - 1
                    track = pygame.mixer.music.load(filelist[file])  
                    pygame.mixer.music.play()  # 播放
                    pause = 0  
                    print(filelist[file])  #輸出歌名
            except ValueError:
                pass
        time.sleep(0.2)  

#Muti-threads  多執行緒宣告
threads=[]  
t1 = threading.Thread(target=playpause)  
threads.append(t1)  
t2 = threading.Thread(target=volume)  
threads.append(t2)  
t3 = threading.Thread(target=switch)  
threads.append(t3)  
t4 = threading.Thread(target=volume_scale)  
threads.append(t4)  
t5 = threading.Thread(target=specify)  
threads.append(t5)  
  
print('Wait......')  
print(filePlaying + 1,filelist[filePlaying])  

if __name__ == '__main__':  
    for t in threads:  
        t.setDaemon(True)  
        t.start()  
    try:
        print('Press Ctrl-C to stop the program')
        while True:
            print('Waiting for RFCOMM channel {} to connect'.format(port))
            client_socket, client_info = server_socket.accept()
            print('Accept connection from {}'.format(client_info))
            try:
                while True:
                    data = client_socket.recv(1024).decode().lower()
                    if len(data) == 0:
                        break
                    #else:
                        #print('command: {}'.format(data))
            except IOError:
                pass
            client_socket.close()
            print('Disconnect')
    except KeyboardInterrupt:
        print('Interrupt program')
    finally:
        if 'client_socket' in vars():
            client_socket.close()
        server_socket.close()
        GPIO.cleanup()
        print('Disconnect')
    
    
    t.join()  

## pygame 功能列表
# pygame.init() 進行全部模組的初始化，
# pygame.mixer.init() 或者只初始化音訊部分
# pygame.mixer.music.load(‘xx.mp3’) 使用檔名作為引數載入音樂 ,音樂可以是ogg、mp3等格式。載入的音樂不會全部放到內容中，而是以流的形式播放的，即在播放的時候才會一點點從檔案中讀取。
# pygame.mixer.music.play()播放載入的音樂。該函式立即返回，音樂播放在後臺進行。
# play方法還可以使用兩個引數
# pygame.mixer.music.play(loops=0, start=0.0) loops和start分別代表重複的次數和開始播放的位置。
# pygame.mixer.music.stop() 停止播放，
# pygame.mixer.music.pause() 暫停播放。
# pygame.mixer.music.unpause() 取消暫停。
# pygame.mixer.music.fadeout(time) 用來進行淡出，在time毫秒的時間內音量由初始值漸變為0，最後停止播放。
# pygame.mixer.music.set_volume(value) 來設定播放的音量，音量value的範圍為0.0到1.0。
# pygame.mixer.music.get_busy() 判斷是否在播放音樂,返回1為正在播放。
# pygame.mixer.music.set_endevent(pygame.USEREVENT 1) 在音樂播放完成時，用事件的方式通知使用者程式，設定當音樂播放完成時傳送pygame.USEREVENT 1事件給使用者程式。
# pygame.mixer.music.queue(filename) 使用指定下一個要播放的音樂檔案，當前的音樂播放完成後自動開始播放指定的下一個。一次只能指定一個等待播放的音樂檔案。