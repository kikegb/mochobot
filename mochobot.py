from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import RPi.GPIO as GPIO
import time

# Config sensor de ultrasonidos
GPIO.setmode(GPIO.BCM)
TRIGGER_PIN = 18
ECHO_PIN = 24
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Función para medir la distancia con el sensor de ultrasonidos
def distancia():
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


# Inicializar el controlador
mh = Adafruit_MotorHAT(addr=0x60)

# Seleccionar los motores que deseas controlar
motor1 = mh.getMotor(1)
motor2 = mh.getMotor(2)

# Definir la velocidad de los motores (0-255)
velocidad = 150

while True:
    # Medir la distancia con el sensor de ultrasonidos
    dist = distancia()

    # Si la distancia es menor a 20cm, detener los motores
    if dist < 20:
        motor1.run(Adafruit_MotorHAT.RELEASE)
        motor2.run(Adafruit_MotorHAT.RELEASE)

    # Si la distancia es mayor a 20cm, mover los motores hacia adelante
    else:
        motor1.run(Adafruit_MotorHAT.FORWARD)
        motor1.setSpeed(velocidad)
        motor2.run(Adafruit_MotorHAT.FORWARD)
        motor2.setSpeed(velocidad)
