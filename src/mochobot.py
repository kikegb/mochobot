import os
import numpy as np
#import cv2
import time
import RPi.GPIO as GPIO
#import picamera
import random

# Definición de rutas a archivos
#rutaActual = os.path.abspath(os.path.dirname(__file__))
#rutaImagen = rutaActual + "/imagen.jpg" # Ruta a la imagen tomada del suelo 

# Configuración de los pines
GPIO.setmode(GPIO.BCM)
# Pins sensor ultrasónico 1
TRIGGER_PIN_ULT1 = 18
ECHO_PIN_ULT1 = 24
# Pins sensor ultrasónico 2
TRIGGER_PIN_ULT2 = 15
ECHO_PIN_ULT2 = 25
# Pins controladora motores 1 (Controla 2 motores)
Contr1_In1 = 13 
Contr1_In2 = 20
Contr1_In3 = 12
Contr1_In4 = 16
# Pins controladora motores 2 (Controla 1 motor)
Contr2_In1 = 6 
Contr2_In2 = 19

# Configuración sensores ultrasonidos
GPIO.setup(TRIGGER_PIN_ULT1, GPIO.OUT)
GPIO.setup(ECHO_PIN_ULT1, GPIO.IN)
GPIO.setup(TRIGGER_PIN_ULT2, GPIO.OUT)
GPIO.setup(ECHO_PIN_ULT2, GPIO.IN)

# Configuración controladoras de motores 
# In1 e In2 controlan rueda derecha trasera | In3 e In4 controlan rueda izquierda trasera | Contr2_In1 y Contr2_In2 controlan rueda delantera
GPIO.setup(Contr1_In1,GPIO.OUT)
motor1 = GPIO.PWM(Contr1_In1,25)
GPIO.setup(Contr1_In2,GPIO.OUT)
GPIO.setup(Contr1_In3,GPIO.OUT)
motor2 = GPIO.PWM(Contr1_In3,25)
GPIO.setup(Contr1_In4,GPIO.OUT)
GPIO.setup(Contr2_In1,GPIO.OUT)
GPIO.setup(Contr2_In2,GPIO.OUT)
# Motores empiezan parados
motor1.start(0)
GPIO.setup(Contr1_In2,GPIO.LOW)
motor2.start(0)
GPIO.setup(Contr1_In4,GPIO.LOW)
GPIO.setup(Contr2_In1,GPIO.LOW)
GPIO.setup(Contr2_In2,GPIO.LOW)

# Funciones control de motores
"""
Funciones que aplican los cambios necesarios a los motores a través
de los pines de la raspberry para que el robot se mueva en una 
dirección concreta
"""
def movDerecha():
    motor1.ChangeDutyCycle(50) 
    GPIO.output(Contr1_In2, GPIO.LOW)    
    motor2.ChangeDutyCycle(50)    
    GPIO.output(Contr1_In4, GPIO.HIGH)   
    GPIO.output(Contr2_In1, GPIO.LOW)
    GPIO.output(Contr2_In2, GPIO.LOW)

def movIzquierda():
    motor1.ChangeDutyCycle(50)  
    GPIO.output(Contr1_In2, GPIO.HIGH)    
    motor2.ChangeDutyCycle(50)   
    GPIO.output(Contr1_In4, GPIO.LOW)   
    GPIO.output(Contr2_In1, GPIO.LOW)
    GPIO.output(Contr2_In2, GPIO.LOW)

def movAtras():
    motor1.ChangeDutyCycle(50) 
    GPIO.output(Contr1_In2, GPIO.HIGH)    
    motor2.ChangeDutyCycle(50)  
    GPIO.output(Contr1_In4, GPIO.HIGH)   
    GPIO.output(Contr2_In1, GPIO.LOW)
    GPIO.output(Contr2_In2, GPIO.LOW)

def movDelante():
    motor1.ChangeDutyCycle(50) 
    GPIO.output(Contr1_In2, GPIO.LOW)    
    motor2.ChangeDutyCycle(50)  
    GPIO.output(Contr1_In4, GPIO.LOW)   
    GPIO.output(Contr2_In1, GPIO.HIGH)
    GPIO.output(Contr2_In2, GPIO.LOW)

def movParar():
    motor1.ChangeDutyCycle(0)
    GPIO.setup(Contr1_In2,GPIO.LOW)
    motor2.ChangeDutyCycle(0)
    GPIO.setup(Contr1_In4,GPIO.LOW)
    GPIO.setup(Contr2_In1,GPIO.LOW)
    GPIO.setup(Contr2_In2,GPIO.LOW)

def movAleatorio():
    movimiento = random.choice([0, 1])
    if movimiento == 0:
        movDerecha()
    else:
        movIzquierda()


# Funciones control sensores ultrasonidos
def distancia(TRIGGER_PIN, ECHO_PIN):
    """
    Función para medir la distancia con el sensor de ultrasonidos
    devuelve la distancia en cm
    """
    # Establecer el trigger a alto
    GPIO.output(TRIGGER_PIN, True)

    # Esperar 0.01ms y luego establecer el trigger a bajo
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    inicio_tiempo = time.time()
    fin_tiempo = time.time()

    # Guardar el tiempo de inicio
    while GPIO.input(ECHO_PIN) == 0:
        inicio_tiempo = time.time()

    # Guardar el tiempo de llegada de la onda reflejada
    while GPIO.input(ECHO_PIN) == 1:
        fin_tiempo = time.time()

    # Calcular la duración del pulso
    duracion = fin_tiempo - inicio_tiempo

    # Calcular la distancia en cm
    distancia = duracion * 17150

    # Retornar la distancia redondeada a 2 decimales
    return round(distancia, 2)


# Creamos instancia de la camara para poder tomar fotos posteriormente
#camara = picamera.PiCamera() 

# Definimos la distancia a la que detener el robot antes de chocar (en cm)
TOPE = 30

#############################################################################
try:
# Bucle de movimiento de mochobot
    while(True):
        # Comprobamos a que distancia estan los objetos del robot
        d1 = distancia(TRIGGER_PIN_ULT1, ECHO_PIN_ULT1)
        d2 = distancia(TRIGGER_PIN_ULT2, ECHO_PIN_ULT2)
        
        if d1 <= TOPE or d2 <= TOPE:
            movParar()
            time.sleep(2)
            movAtras()
            time.sleep(2)
            movParar()
            time.sleep(2)
            movAleatorio()
            time.sleep(1)
            movParar()
            time.sleep(2)
            movDelante()
        else:
            #if os.path.exists(rutaImagen):
            #	os.remove(rutaImagen)
            #camara.capture(rutaImagen)
            #analisisManchas()
            movDelante()
        
        time.sleep(0.25) 
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    #camara.close()
