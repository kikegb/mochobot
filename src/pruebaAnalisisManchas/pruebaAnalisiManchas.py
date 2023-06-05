import os
import numpy as np
import cv2
import shutil
from detect import run

# Definición de rutas a archivos
rutaActual = os.path.abspath(os.path.dirname(__file__))
rutaModelo = rutaActual + "/best.pt" # Ruta a modelo entrenado para YoloV5. Datos obtenidos de: https://uapt33090-my.sharepoint.com/personal/danielduartecanedo_ua_pt/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fdanielduartecanedo%5Fua%5Fpt%2FDocuments%2Fgenerated%5Fdataset&ga=1
rutaMancha = rutaActual + "/posicionMancha.txt" # Ruta a archivo que guarda la posición de la mancha actual
rutaResultado = rutaActual + "/runs/detect/exp" # Ruta a carpeta que contiene la imagen con las manchas detectadas
rutaImagen = rutaActual + "/imagen.jpg" # Ruta a la imagen tomada del suelo 

# Funciones detección manchas en el suelo
def posicionMancha(sizeImg, x, rango=20):
    """
    Función que determina hacia donde se desplazará mochobot,
    según la ubicación de la mancha en la imagen.
    return val
    val = 0 -> Desplazamiento a la izquierda
    val = 1 -> Desplazamiento a la derecha
    val = 2 -> Continuar recto
    """
    anchoImg, _ = sizeImg
    centroImg = anchoImg / 2

    # Definicion de límite de detección del centro de la imagen
    rangoIzquierda = centroImg - rango
    rangoDerecha = centroImg + rango

    val = -1

    if x < rangoIzquierda:
        posicion_horizontal = "más a la izquierda"
        val = 0
    elif x > rangoDerecha:
        posicion_horizontal = "más a la derecha"
        val = 1
    else:
        posicion_horizontal = "en el centro"
        val = 2

    print(f"El punto está {posicion_horizontal}")
    return val

def mostrarUbicacionMancha(imagen, x, y):
    """
    Muestra un punto rojo donde se ha detectado la mancha
    """
    colorRojo = (0, 0, 255)  
    grosor = 5
    cv2.circle(imagen, (int(x), int(y)), grosor, colorRojo, -1)

    cv2.imshow('Imagen', imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def analisisManchas():
    """
    Función que busca manchas en el suelo, de la foto tomada por la camara
    y decide en que dirección debe desplazarse mochobot
    return direccion
    """

    # Elimina los resultados anteriores si los hay
    if os.path.exists(rutaResultado):
        shutil.rmtree(rutaResultado)
    if os.path.exists(rutaMancha):
        os.remove(rutaMancha)

    if os.path.exists(rutaImagen):
        # Detecta las manchas y crea un archivo con la posición de una mancha detectada
        # y una imagen nuevo con las manchas detectadas
        run(
            weights=rutaModelo,
            imgsz=(640, 640),
            conf_thres=0.50,
            source=rutaImagen
        )

        # Significa que no se ha detectado mancha
        if not os.path.exists(rutaMancha): 
            posicion = 2 # Continua recto
            print("No se ha detectado mancha")
        else:
            #Imagen generada por YoloV5
            cv2.imshow('Imagen YoloV5', cv2.imread(rutaResultado + '/imagen.jpg'))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # Leer las coordenadas desde el archivo de texto
            with open(rutaMancha, 'r') as archivo:
                contenido = archivo.readlines()

            coordenadas = [float(valor.strip()) for valor in contenido]

            # Cargar la imagen de las manchas detectadas
            imagen = cv2.imread(rutaImagen)

            # Extrae las coordenadas 
            x, y, w, h = coordenadas

            # Punto rojo que indica ubicacion de la mancha con la que se queda (donde empieza el recuadro generado por Yolov5)
            mostrarUbicacionMancha(imagen, x, y)

            # Se decide en que dirección se tiene que despazar mochobot
            posicion = posicionMancha(imagen.shape[:2], x)

            # Toma de decisión sobre el desplazamiento
            """if posicion == 0:
                movIzquierda()
            elif posicion == 1:
                movDerecha()
            elif posicion == 2:
                movDelante()
            else:
                movParar()
            time.sleep(0.5)"""
    else:
        print("No hay imagen para procesar guardada")