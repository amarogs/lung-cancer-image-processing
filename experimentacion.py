import os as os
import radiomics as rad
import pandas as pd
from funciones import *

"""Variables globales """

DIR_BASE = "./Lung Phantom"
CARPETA_NODULO = "1000-QIN"

"""Funciones para el procesado de carpetas """

def busca_carpetas(direct):
    return [c for c in os.listdir(direct) if c[0] != "."]


def listado_directorio_imagenes():
    """Devuelve una lista de listas. Cada lista individual consiste en una serie de Strings que contienen
    la ruta relativa a las distintas carpetas para un mismo paciente. """
    global DIR_BASE

    listado_imagenes = []

    for carpeta_paciente in busca_carpetas(DIR_BASE):
        siguiente = DIR_BASE + "/" + carpeta_paciente
        siguiente = siguiente + "/" + busca_carpetas(siguiente)[0]
        paciente = [siguiente + "/" + d for d in busca_carpetas(siguiente)]
        listado_imagenes.append(paciente)

    return listado_imagenes


def leer_paciente(carpeta_paciente):
    """Recibe una lista de String con los archivos de un paciente (imagenes dicom y diferentes pruebas), 
    lee cada imagen devolviendo un par (img_paciente, [img_nodulo]) donde el primer elemento es el TAC
    en formato sitk sin procesar y el segundo es una lista de máscaras sitk del nódulo del paciente
    obtenido mediante diferentes algoritmos."""

    global CARPETA_NODULO

    img_paciente = None
    img_nodulos = []

    for carpeta in carpeta_paciente:

        if carpeta.split("/")[-1].startswith(CARPETA_NODULO):
            img_nodulos.append(leer_una_imagen(carpeta))
        else:
            img_paciente = leer_dicom(carpeta)
    return img_paciente, img_nodulos


def caracteristicas_nodulo(img_paciente, mascara, id_paciente, id_prueba):
    """Dada una imagen sitk del paciente y una máscara del nódulo se extraen las características
    estadísticas del nódulo. """

    #Creamos el extractor de caracteristicas
    extractor = rad.featureextractor.RadiomicsFeatureExtractor()
    extractor.disableAllFeatures()
    extractor.enableFeaturesByName(glcm=["JointEnergy"], shape=[
                                   'Sphericity', 'Elongation'])

    #Extraemos las caracteristicas de la mascara
    
    result = extractor.execute(img_paciente, mascara, label=1)

    sphericity = result['original_shape_Sphericity']
    elongation = result['original_shape_Elongation']
    energy = result['original_glcm_JointEnergy']
    
    return (id_paciente,id_prueba,sphericity, elongation, energy)


def datos_estadisticos_nodulo(listado_dir_imagenes, archivo_salida):
    """Recibe la imagen de un paciente y la lista de máscaras del nódulo para extraer datos
    estadisticos que se guardan en la lista global DATOS. """

    nombres = ["paciente", "prueba", "sphericity", "elongation", "energy"]
    datos = []

    for (id_paciente, carpeta_paciente) in enumerate(listado_dir_imagenes):
        img_paciente, lista_nodulos = leer_paciente(carpeta_paciente)

        for (id_prueba, nodulo) in enumerate(lista_nodulos):
            nodulo = sitk.GetImageFromArray(nodulo)
            nodulo.CopyInformation(img_paciente)
            datos.append(caracteristicas_nodulo(img_paciente,nodulo,id_paciente, id_prueba))
    

    dataframe = pd.DataFrame(data=datos, columns=nombres)
    dataframe.to_excel("./"+archivo_salida+".xls")

def experimentacion_watershed(listado_dir_imagenes, niveles_ws):


    for (id_paciente, carpeta_paciente) in enumerate(listado_dir_imagenes):
        for (id_paciente, carpeta_paciente) in enumerate(listado_dir_imagenes):
            img_paciente, lista_nodulos = leer_paciente(carpeta_paciente)
            mostrar_slice(img_paciente)
            seeds = obtener_semilla_automatica(img_paciente)
            print(seeds, [img_paciente.GetPixel(s) for s in seeds])
            

#Lista de lista donde cada elemento son rutas a información de un paciente
listado_dir_imagenes = listado_directorio_imagenes()

#datos_estadisticos_nodulo(listado_dir_imagenes, "prueba")



  
