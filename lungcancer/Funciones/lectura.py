import os
import SimpleITK as sitk
import pydicom

"""Funciones para el procesado de carpetas """
CARPETA_NODULO = "1000-QIN"


def leer_una_imagen(directorio):
    """Dada el directorio de una imagen, la carga como imagen de numpy """

    files = []
    for fname in os.listdir(directorio):

        if fname[-3::] == "dcm":
            files.append(pydicom.read_file(directorio+"/"+fname))

    return files[0].pixel_array


def leer_dicom(directorio):
    """Dado un directorio, lee toda la serie dicom de un TAC """
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(directorio)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    img_re = sitk.RescaleIntensity(image, -1024, 3071)

    return img_re

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
