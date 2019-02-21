import RPi.GPIO as GPIO

import time

servo = 5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo, GPIO.OUT)
pwm=GPIO.PWM(servo, 50)


pwm.start(0)

#-------------Função para controle do servo----------------
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
        

while True:

    feed(5)
    time.sleep(10)


pwm.stop()
GPIO.cleanup()


# Ao passar para o codigo principal nao esquecer:

        # NO ESCOPO GLOBAL:
        # 
        # GPIO.setup(servo, GPIO.OUT)
        # pwm=GPIO.PWM(servo, 50)
        # pwm.start(0)
        # funções servo_spin() e feed()


        # NO WHILE:
        # feed(5)
        # pwm.stop()
        # GPIO.cleanup() no final da função while
        
