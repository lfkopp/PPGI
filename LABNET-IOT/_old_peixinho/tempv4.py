import RPi.GPIO as GPIO, os, telepot, time, numpy as np, cv2, glob
from urllib.request import urlopen
from telepot.loop import MessageLoop


fish_cascade = cv2.CascadeClassifier('peixinhos.xml')

thingspeak_api = 'Y8VNVETDNZQ4EBRA'
baseURL = 'https://api.thingspeak.com/update?api_key=' + thingspeak_api
telegram_token = '445110681:AAG1sEVjzZ2vRbJuTaKOuM8UlSytOAsIttc'
usuario = 126554909
redPin, greenPin, bluePin  = 11, 13, 15
bombaPIN, lightPIN, coolerPIN = 36, 38, 40
pin_to_circuit = 7
temp_amb, light, temp = -1,-1, -1
time_control = 0 #time.time()

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder1 = glob.glob(base_dir + '28*')[0]
device_file1 = device_folder1 + '/w1_slave'

device_folder2 = glob.glob(base_dir + '28*')[1]
device_file2 = device_folder2 + '/w1_slave'

modo_bomba, modo_cooler, modo_lampada = "auto", "auto", "auto"
status_bomba, status_cooler, status_lampada = "on", "on", "on"
modo_tracker = "off"


#função para acionar bomba    
def bomba(modo):
    global status_bomba, modo_bomba
    if modo == "on":
        GPIO.output(bombaPIN,0)
        status_bomba = "on"
    elif modo == "off":
        GPIO.output(bombaPIN,1)
        status_bomba = "off"
    print("modo_bomba",modo_bomba)
    return

#Função para acionar lampadas led
def luz_led(modo):
    global status_lampada, modo_lampada
    if modo == "on":
        GPIO.output(lightPIN,0)
        status_lampada = "on"
    elif modo == "off":
        GPIO.output(lightPIN,1)
        status_lampada = "off"
    print("modo_lampada",modo_lampada)
    return

#Função para acionar cooler
def cooler(modo):
    global status_cooler, modo_cooler
    if modo == "on":
        GPIO.output(coolerPIN,0)
        status_cooler = "on"
    elif modo == "off":
        GPIO.output(coolerPIN,1)
        status_cooler = "off"
    print("modo_cooler",modo_cooler)
    return
 
def read_temp_raw(device_file):
  f = open(device_file, 'r') 
  lines = f.readlines()
  f.close()
  return lines
 
def read_temp(device_file):
  lines = read_temp_raw(device_file)
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

GPIO.setup(bombaPIN, GPIO.OUT)
GPIO.setup(lightPIN, GPIO.OUT)
GPIO.setup(coolerPIN, GPIO.OUT)


def relays_init():
    #atuadores ligando em estado baixo
    GPIO.output(bombaPIN, GPIO.LOW)  
    GPIO.output(lightPIN, GPIO.LOW)
    GPIO.output(coolerPIN, GPIO.LOW)
relays_init()


def led_off():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.LOW)
led_off()

def handle(msg):
    global status_bomba, modo_bomba, status_cooler, modo_cooler, status_lampada, modo_lampada
    content_type, chat_type, chat_id = telepot.glance(msg)
    ##print(content_type, chat_type, chat_id)
    if content_type == 'text':
        txt = msg['text'].upper()
        print(chat_id, txt)
        if (txt == 'START') or (txt == '/START'):
            bot.sendMessage(chat_id, 'comandos: FOTO RED GREEN BLUE OFF FEED INFO STATUS')
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
        elif txt == 'FOTO':
            cv2.imwrite('fish.png',img)
            bot.sendPhoto(chat_id, open('fish.png', 'rb'))
        elif txt == 'FEED':
            bot.sendMessage(chat_id, 'Peixinhos alimentados')
        elif txt == 'INFO':
            bot.sendMessage(chat_id, ("luz=%s, temp_cpu=%s, hora_init=%s, hora=%s, temp_amb=%s, temp_aq=%s" % (light,temp,hora_init,hora(),temp_amb,temp_aquario)))  
        elif txt == 'STATUS':
            bot.sendMessage(chat_id, ("bomba=%s, cooler=%s, lampada=%s" % (status_bomba, status_cooler, status_lampada)))  
        elif txt == 'MODO':
            bot.sendMessage(chat_id, ("bomba=%s, cooler=%s, lampada=%s" % (modo_bomba, modo_cooler, modo_lampada)))  
        elif txt == 'BOMBAAUTO':
            modo_bomba = "auto"
            bot.sendMessage(chat_id, 'Bomba em automático')            
        elif txt == 'BOMBAON':
            bomba("on")
            modo_bomba = "on"
            bot.sendMessage(chat_id, 'Bomba ligada')
        elif txt == 'BOMBAOFF':
            bomba("off")
            modo_bomba = "off"
            bot.sendMessage(chat_id, 'Bomba desligada')
        elif txt == 'COOLERAUTO':
            modo_cooler = "auto"
            bot.sendMessage(chat_id, 'Cooler em automático')   
        elif txt == 'COOLERON':
            cooler("on")
            modo_cooler = "on"
            bot.sendMessage(chat_id, 'cooler ligada')
        elif txt == 'COOLEROFF':
            cooler("off")
            modo_cooler = "off"
            bot.sendMessage(chat_id, 'cooler desligada')
        elif txt == 'LAMPADAAUTO':
            modo_lampada = "auto"
            bot.sendMessage(chat_id, 'Lampada em automático')   
        elif txt == 'LAMPADAON':
            luz_led("on")
            modo_lampada = "on"
            bot.sendMessage(chat_id, 'iluminação ligada')
        elif txt == 'LAMPADAOFF':
            luz_led("off")
            modo_lampada = "off"
            bot.sendMessage(chat_id, 'iluminação desligada')
        else:
            bot.sendMessage(chat_id, 'comando não compreendido. \n comandos possíveis: FOTO RED GREEN BLUE OFF FEED INFO STATUS')            
            
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


fishes = [(1,1,1,1)]
while True:
    try:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        try:
            fishes = fish_cascade.detectMultiScale(gray)
        except: pass
        for (x,y,w,h) in fishes:
                if (w < 70 and w > 2 and h > 2) :
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
        cv2.putText(img,("%s %s %s %s %s %s" % (light,temp,hora_init,hora(),temp_amb,temp_aquario)),(20,30), font, .5,(0,0,255),2)
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
            temp_amb     = read_temp(device_file2)
            temp_aquario = read_temp(device_file1)
            try:
                f = urlopen(baseURL + "&field1=%s&field2=%s&field3=%s&field4=%s" % (light,temp,temp_amb,temp_aquario))
                print(hora(), f.read(), light, temp, temp_amb,temp_aquario)
                f.close()
            except:
                print(hora(), "erro ao enviar para thingspeak")
        
            #### temperatura automatica
            if modo_cooler == "auto":
                if temp > 55:
                    cooler("on")
                elif temp < 45:
                    cooler("off")
            else:
                cooler(modo_cooler)
            if temp > 70:
                print(hora(), "temperatura acima do normal")
                cooler("on")
                bot.sendMessage(usuario, ("temp_cpu=%s" % (temp)))
                time.sleep(45)
   
            #### lampada automatica
            if modo_lampada == "auto":
                if light > 400:
                    luz_led("on")
                elif light < 100:
                    luz_led("off")   
            else:
                luz_led(modo_lampada)


    except:
        pass
    
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
