import RPi.GPIO as GPIO, os, telepot, time, numpy as np, cv2, glob
from urllib.request import urlopen
from telepot.loop import MessageLoop

thingspeak_api = 'Y8VNVETDNZQ4EBRA'
baseURL = 'https://api.thingspeak.com/update?api_key=' + thingspeak_api
telegram_token = '445110681:AAG1sEVjzZ2vRbJuTaKOuM8UlSytOAsIttc'
usuario = 126554909
redPin, greenPin, bluePin  = 11, 13, 15
pin_to_circuit = 7
temp_amb, light, temp = -1,-1, -1
time_control = 0 #time.time()

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
  f = open(device_file, 'r') 
  lines = f.readlines()
  f.close()
  return lines
 
def read_temp():
  lines = read_temp_raw()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw()
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    return str(temp_c)

def hora():
    return str(time.strftime("%d/%m/%y %H:%M:%S", time.localtime(time.time())))

hora_init = hora()
bot = telepot.Bot(telegram_token)
print(hora_init, bot.getMe())
bot.sendMessage(usuario, 'Hey! iniciando')

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

def led_off():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.LOW)
led_off()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    ##print(content_type, chat_type, chat_id)
    if content_type == 'text':
        txt = msg['text'].upper()
        print(chat_id, txt)
        if (txt == 'START') or (txt == '/START'):
            bot.sendMessage(chat_id, 'comandos: RED GREEN BLUE OFF FEED INFO')
        elif txt == 'RED':
            GPIO.output(redPin, GPIO.HIGH)
            bot.sendMessage(chat_id, 'LED ligado') 
        elif txt == 'GREEN':
            GPIO.output(greenPin, GPIO.HIGH)
            bot.sendMessage(chat_id, 'LED ligado')
        elif txt == 'BLUE':
            GPIO.output(bluePin, GPIO.HIGH)
            bot.sendMessage(chat_id, 'LED ligado')
        elif txt == 'OFF':
            led_off()
            bot.sendMessage(chat_id, 'LED desligado')
        elif txt == 'FEED':
            cv2.imwrite('fish.png',img)
            bot.sendPhoto(chat_id, open('fish.png', 'rb'))
            bot.sendMessage(chat_id, 'Peixinhos alimentados')
        elif txt == 'INFO':
            bot.sendMessage(chat_id, ("luz=%s, temp_cpu=%s, hora_init=%s, hora=%s, temp=%s" % (light,temp,hora_init,hora(),temp_amb)))  
        else:
            bot.sendMessage(chat_id, 'comando não compreendido. \n comandos possíveis: RED GREEN BLUE OFF FEED INFO')            
            
def rc_time (pin_to_circuit):
    count = 0
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin_to_circuit, GPIO.IN)
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
    return count

MessageLoop(bot, handle).run_as_thread()



while True:
    try:
        _, img = cap.read()
        cv2.putText(img,("%s %s %s %s %s" % (light,temp,hora_init,hora(),temp_amb)),(20,30), font, .5,(0,0,255),2)
        cv2.imshow('img',img)
        cv2.waitKey(1) & 0xff
    except:    
        print(hora, "erro na camera")
    
    try:
        if(time.time() > time_control +15):
            time_control = time.time() 
            light= np.round(rc_time(pin_to_circuit)**.5,1)
            temp = np.round(float(os.popen('vcgencmd measure_temp')
                         .readline().replace("temp=","")
                         .replace("'C\n","")),1)
            temp_amb = read_temp()
            try:
                f = urlopen(baseURL + "&field1=%s&field2=%s&field3=%s" % (light,temp,temp_amb))
                print(hora(), f.read(), light, temp, temp_amb)
                f.close()
            except:
                print(hora(), "erro ao enviar para thingspeak")
        
        ## Setting up alarm system
            if temp > 70:
                print(hora(), "temperatura acima do normal")
                bot.sendMessage(usuario, ("temp_cpu=%s" % (temp)))
                time.sleep(45)   

    except:
        pass
    
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()