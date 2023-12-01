from machine import PWM, Pin, ADC
import time

def alimentador(g,fr,actb,fuente):   #g,fr=salida   x,y=entrada sensores

    servo=PWM(Pin(26))
    servo.freq(50)

    bomba = Pin(14,Pin.OUT)
    bomba.value(0)

    led_on= Pin(5,Pin.OUT)
    led_on.value(1)
    led_2= Pin(21,Pin.OUT)
    led_2.value(0)
    #falta los leds

    luz_plato = Pin(2, Pin.IN)
    adc1 = ADC(luz_plato)        
    luz_comida = Pin(4, Pin.IN)
    adc2 = ADC(luz_comida)
    buzzer = Pin(33,Pin.OUT)
    buzzer.value(0)


    s = g*500      #convertir de gramos a tiempo de operacion
    #s(t) segun este tiempo varia la cantidad de comida que sale
    t_limite_servo=time.ticks_add(time.time(), fr*10)   #fr=cada cuantas horas se alimenta al gato(*3600)
    
    tb = actb*5+fuente*10                                #tb=tiempo que dura la bomba activada (fuente=*15min=*900s)
    t_limite_b = time.ticks_add(time.time(), actb*5)   #actb=cada cuanto se activa la fuente(*1800=30min)
    t_off_b = time.ticks_add(time.time(), tb)        
    
    while True:
        #fuente
        if time.ticks_diff(t_limite_b, time.time()) <= 0:
            bomba.value(1)

        if time.ticks_diff(t_off_b, time.time()) <= 0:        
            bomba.value(0)
            t_off_b = time.ticks_add(time.time(), tb)       #recupera tiempo              
            t_limite_b = time.ticks_add(time.time(), actb*5)  #recupera tiempo
            
            
        #comida
        if time.ticks_diff(t_limite_servo, time.time()) <= 0:
            led_2.value(1)#prender el led un tiempo
            time.sleep(1)
            val_plato = adc1.read_u16()
            val_comida = adc2.read_u16()
            led_2.value(0) #apagar led
            if val_comida>40000:
                buzzer.value(1)
                time.sleep(1)
                buzzer.value(0)
                time.sleep(1)
                buzzer.value(1)
                time.sleep(1)
                buzzer.value(0)
                time.sleep(1)
                buzzer.value(1)
                time.sleep(1)
                buzzer.value(0)
                t_limite_servo=time.ticks_add(time.time(), fr*10)
            else:
                if val_plato>10000:
                    
                    if servo.duty() == 72:        # si esta en 0 grados
                        servo.duty(20)
                        time.sleep_ms(s)
                        servo.duty(72)
                    else:                          
                        servo.duty(72)                # se pone en 0 grados
                t_limite_servo=time.ticks_add(time.time(), fr*10)  #recupera fr

x=3
y=1
d=1
a=1
'''
x=int(input('gramos'))
y=int(input('frecuencia con la que alimentar(h)'))
d=int(input('frecuencia de activacion de la fuente(*30min)'))
a=int(input('tiempo de funcionamiento fuente(*15min)'))
'''
alimentador(x,y,d,a)