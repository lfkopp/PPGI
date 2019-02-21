#import RPi.GPIO as GPIO, os, telepot, time, numpy as np, cv2, glob
#from urllib.request import urlopen
import telepot,cv2, os, numpy as np
from telepot.loop import MessageLoop

thingspeak_api = 'Y8VNVETDNZQ4EBRA'
baseURL = 'https://api.thingspeak.com/update?api_key=' + thingspeak_api
telegram_token = '445110681:AAG1sEVjzZ2vRbJuTaKOuM8UlSytOAsIttc'
usuario = 126554909
try:
    bot = telepot.Bot(telegram_token)
    bot.sendMessage(usuario, 'Hey! iniciando')
except:
    print("erro envio iniciando")

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
font = cv2.FONT_HERSHEY_SIMPLEX
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', 640, 480)

cv2.namedWindow('img2', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img2', 640, 480)


def handle(msg):
    try:
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
          txt = msg['text'].upper()
          print(chat_id, txt)
          if txt == '/SALA':
            cv2.imwrite('foto.png',img)
            bot.sendPhoto(chat_id, open('foto.png', 'rb'))
            cv2.imwrite('foto2.png',img2)
            bot.sendPhoto(chat_id, open('foto2.png', 'rb'))
            bot.sendMessage(chat_id, str(temp))
    except:
        pass
MessageLoop(bot, handle).run_as_thread()

while True:
    _, img = cap.read()
    _, img2 = cap2.read()
    cv2.imshow('img',img)
    cv2.imshow('img2',img2)
    temp = np.round(float(os.popen('vcgencmd measure_temp')
                 .readline().replace("temp=","")
                 .replace("'C\n","")),1)
    if temp > 65:
        espera = 1000
    else:
        espera = 1
    cv2.waitKey(espera) & 0xff
  
cap.release()
cv2.destroyAllWindows()
