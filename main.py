import os.path
from pprint import pprint
import time
from io import BytesIO
from random import random
import uuid

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
import azure.cognitiveservices.vision.contentmoderator.models
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.contentmoderator.models import (
    Screen
)
CONTENT_MODERATOR_ENDPOINT = os.environ.get("CONTENT_MODERATOR_ENDPOINT")
subscription_key = os.environ.get("CONTENT_MODERATOR_SUBSCRIPTION_KEY")

client = ContentModeratorClient(
    endpoint=CONTENT_MODERATOR_ENDPOINT,
    credentials=CognitiveServicesCredentials(subscription_key)
)
def analizar_texto(nombre_archivo_txt, idioma):
    TEXT_FOLDER = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "Texto")

    # Screen the input text: check for profanity,
    # do autocorrect text, and check for personally identifying
    # information (PII)
    with open(os.path.join(TEXT_FOLDER, nombre_archivo_txt), "rb") as text_fd:
        screen = client.text_moderation.screen_text(
            text_content_type="text/plain",
            text_content=text_fd,
            language=idioma,
            autocorrect=True,
            pii=True,
            classify = True
        )
        assert isinstance(screen,Screen)
        texto_analizado = screen.as_dict()
        return texto_analizado
        
def contenido_sensible(texto, idioma):
    texto_analizado = analizar_texto(texto,idioma)
    if "terms" in texto_analizado:
        print("En este texto aparecen malas palabras")
        respuesta = input("Si desea conocer estos términos presione A, si no presione cualquier tecla ")
        if respuesta == "A":
            for palabra in texto_analizado["terms"]:
                print("La palabra es: ", palabra["term"])
    else:
        print("No hay contenido sensible")
 
 #solo funciona para inglés
def clasificar_contenido(texto, idioma):
    texto_analizado = analizar_texto(texto,idioma)
    texto_clasificado = texto_analizado["classification"]
    if texto_clasificado["review_recommended"] == True:
        print("Recomendamos analizar este texto, puede tener contenido, sexual u ofensivo")
        if texto_clasificado["category1"]["score"] > 0.50:
            print("Con una precisión de ",round(texto_clasificado["category1"]["score"],2)," este texto tiene contenido considerado sexual explícito o considerado para adultos")
        if texto_clasificado["category2"]["score"] > 0.50:
            print("Con una precisión de ",round(texto_clasificado["category2"]["score"],2)," este texto tiene contenido considerado sugestivo sexual o solo para adultos")
        if texto_clasificado["category3"]["score"] > 0.50:
            print("Con una precisión de ",round(texto_clasificado["category3"]["score"],2)," este texto tiene contenido considerado ofensivo en diferentes circunstancias")
    else:
        print("Es proobable que este archivo no tenga contenido sensible")      

#El tamño máximo de texto es 1024 caracteres
#https://docs.microsoft.com/en-us/azure/cognitive-services/content-moderator/language-support, aquí se pueden consultar los lenguajes soportados
contenido_sensible("eminemsong.txt","eng")#spa para español, eng para inglés
clasificar_contenido("eminemsong.txt","eng")
#contenido_sensible("texto_prueba_espanol.txt","spa")

