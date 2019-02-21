
#versao 5.0
#- incluido o sensor de nivel

#versao 5.0rev
#- incluido alerta  por mensagem no telegram e desliga cooler, led e bomba
#- faceon e faceoff para alternar reconhecimento facial dos peixinhos




import RPi.GPIO as GPIO, os, telepot, time, numpy as np, cv2, glob
from urllib.request import urlopen
from telepot.loop import MessageLoop

#https://api.thingspeak.com/update?api_key=Y8VNVETDNZQ4EBRA
fish_cascade = cv2.CascadeClassifier('peixinhos.xml')

thingspeak_api = 'Y8VNVETDNZQ4EBRA'
baseURL = 'https://api.thingspeak.com/update?api_key=' + thingspeak_api
telegram_token = '445110681:AAG1sEVjzZ2vRbJuTaKOuM8UlSytOAsIttc'
usuario = 126554909
temp_aquario = 0
redPin, greenPin, bluePin  = 36, 38, 40
bombaPIN, lightPIN, coolerPIN = 33, 35, 31
nivelPin = 5
pin_to_circuit = 11
servo = 7 # adicionado na versao 7
temp_amb, light, temp = -1,-1, -1
time_control = 0 #time.time()

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

try: 
    base_dir = '/sys/bus/w1/devices/'
    device_folder1 = glob.glob(base_dir + '28*')[0]
    device_file1 = device_folder1 + '/w1_slave'

    device_folder2 = glob.glob(base_dir + '28*')[1]
    device_file2 = device_folder2 + '/w1_slave'
except:
    pass


modo_bomba, modo_cooler, modo_lampada = "auto", "auto", "auto"
status_bomba, status_cooler, status_lampada, face = "on", "on", "on", "off"
modo_tracker = "off"
modo_feed = "auto"

feed_time = time.time()
feed_period = 12*60*60 #12 horas





###------ Variaveis para uso do sensor de nivel -----------

time_alerta_1 = time.time() #momento do primeiro alerta
count_low = 0 #contagem de leituras de nivel baixo
count_high = 0 #contagem de leitura de nivel normal
limit_time = 10 #tempo limite para alerta 2 em segundos

#----------------------------------------------------------


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


#Função para leitura do nivel---------------------------------------


def get_level():

    global status_level
    nivel = GPIO.input(nivelPin)
    if nivel:
      status_level = "ok"
    else:
      status_level = "baixo"
      
    return str(status_level)

## -------------------------------------------------------------------    
 
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
    print("temp_c" % temp_c)
    return str(temp_c)

def hora():
    return str(time.strftime("%d/%m/%y %H:%M:%S", time.localtime(time.time())))

def sohora():
    return int(time.strftime("%H", time.localtime(time.time())))

hora_init = hora()
bot = telepot.Bot(telegram_token)
print(hora_init, bot.getMe())
bot.sendMessage(usuario, 'Hey! iniciando')

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', 640, 480)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(servo, GPIO.OUT)
pwm=GPIO.PWM(servo, 50)

GPIO.setup(bombaPIN, GPIO.OUT)
GPIO.setup(lightPIN, GPIO.OUT)
GPIO.setup(coolerPIN, GPIO.OUT)

GPIO.setup(nivelPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#----------------- v7 funções servo motor ----------
pwm.start(0)

def servo_spin(angle, time_pause):

      duty = (angle / 18) + 2
      GPIO.output(servo, True)
      pwm.ChangeDutyCycle(duty)
      time.sleep(time_pause)
      GPIO.output(servo, False)
      pwm.ChangeDutyCycle(0)


            
def feed(shake_times):

      servo_spin(0, 1) #posição de alimentação

      for x in range(0, shake_times): #balanço em torno do ponto de alimentação
            servo_spin(30, 0.3) 
            servo_spin(0, 0.3)

      servo_spin(120, 1) #posição de repouso


#----------------------------------------------------------
 


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

def shutdown():
    global status_bomba, modo_bomba, status_cooler, modo_cooler, status_lampada, modo_lampada, status_level
    modo_bomba, modo_lampada, modo_cooler = "off", "off", "off"
    luz_led("off")
    bomba("off")
    cooler("off")
    led_off()

def handle(msg):
    global face, status_bomba, modo_bomba, status_cooler, modo_cooler, status_lampada, modo_lampada, status_level
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
      elif txt == 'FEEDNOW':
        bot.sendMessage(chat_id, 'Peixinhos alimentados')
        if modo_bomba =="off":       
            feed(3)
        else:
            bomba("off")
            feed(3)
            bomba("on")
      elif txt == 'FEEDOFF':
        bot.sendMessage(chat_id, 'Alimentação automatica desligada')
        modo_feed = "off"
      elif txt == 'FEEDAUTO':
        bot.sendMessage(chat_id, 'Alimentação automatica ligada')
        modo_feed = "auto"
      elif txt == 'INFO':
        bot.sendMessage(chat_id, ("luz=%s, temp_cpu=%s, hora_init=%s, hora=%s, temp_amb=%s, temp_aq=%s, level_aq=%s" % (light,temp,hora_init,hora(),temp_amb,temp_aquario, get_level())))  
      elif txt == 'STATUS':
        bot.sendMessage(chat_id, ("bomba=%s, cooler=%s, lampada=%s, face=%s" % (status_bomba, status_cooler, status_lampada, face)))
      elif txt == 'MODO':
        bot.sendMessage(chat_id, ("bomba=%s, cooler=%s, lampada=%s" % (modo_bomba, modo_cooler, modo_lampada)))  
      elif txt == 'BOMBAAUTO':
        modo_bomba = "auto"
        bot.sendMessage(chat_id, 'Bomba em automático')        
      elif txt == 'BOMBAON':        
        modo_bomba = "on"
        bomba("on")
        bot.sendMessage(chat_id, 'Bomba ligada')
      elif txt == 'BOMBAOFF':
        modo_bomba = "off"
        bomba("off")        
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
      elif txt == 'FACEON':
        face = "on"
        bot.sendMessage(chat_id, 'face ligada')
      elif txt == 'FACEOFF':
        face = "off"
        bot.sendMessage(chat_id, 'face desligada')
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
      #else:
        #bot.sendMessage(chat_id, 'comando não compreendido. \n comandos possíveis: FOTO RED GREEN BLUE OFF FEED INFO STATUS')
        
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
      if face == "on":
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
        print("entrou no 15 segundos")
        time_control = time.time()
        print("passou time_control")
        light= np.round(rc_time(pin_to_circuit)**.5,1)
        print("passou de light")
        temp = np.round(float(os.popen('vcgencmd measure_temp')
                 .readline().replace("temp=","")
                 .replace("'C\n","")),1)
        print("passou de temp")
        try:
            temp_amb     = read_temp(device_file2)
            print("passou de temp_amb")
            temp_aquario = read_temp(device_file1)
            print("pré try")
        except:
            pass
        try:
            print("conseguiu")
            f = urlopen(baseURL + "&field1=%s&field2=%s&field3=%s&field4=%s" % (light,temp,temp_amb,temp_aquario))
            print(hora(), f.read(), light, temp, temp_amb,temp_aquario)
            print("enviado ao thingspeak")
            f.close()
        except:
            print("nao conseguiu")
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
            if light > 400 and sohora() > 5:
              luz_led("on")
            elif light < 100 or sohora() < 5:
              luz_led("off")   
        else:
            luz_led(modo_lampada)

        #### alimentação automatica
        if modo_feed == "auto":
            if (time_control - time_feed) > feed_period:
                feed(3)
                time_feed = time_control

        ### Sensor de nivel
        if status_level == "ok": #leitura de nivel ok
            count_high = count_high + 1
            if (count_low > 0) and ((time_control - time_alerta_1) > limit_time):
                print("O nivel voltou ao normal")
                count_low = 0

        elif status_level == "baixo": # leitura de nivel baixo
            
            count_low = count_low + 1
            time_low = time_control
            dif_alerta_1 = time_low - time_alerta_1

            if count_low == 1: #se for primeiro aviso
              
             print("ALERTA: o nivel baixou")
             bot.sendMessage(usuario, 'ALERTA: o nivel baixou')
             time_alerta_1 = time_low
             count_high = 0
            
            elif count_low > 1: 

              
              if (time_control - time_alerta_1) > limit_time: #apos passado tempo limite do primeiro alerta

                if count_high == 0: #se nivel nao tiver voltado ao normal
                    print("Alerta: o nível não voltou ao normal")
                    time_alerta_2 = time_control
                    count_low = 0
                    count_high = 0

                elif count_high > 0: #se tiver oscilado o nivel
                    print("Nível estava oscilando")
                    count_low = 0
                    count_high = 0

        ### fim sensor de nivel


    except:
      pass
    
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()


#bomba no automatio liga 5 desliga 1