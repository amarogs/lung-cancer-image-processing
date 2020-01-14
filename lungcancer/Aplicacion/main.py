import numpy as np
import radiomics as rad
import SimpleITK as sitk


from lungcancer.Experimentacion import experimentacion
from lungcancer.Funciones import funciones, lectura

directorio_paciente = None
paciente_sitk = None  # DICOM del paciente en formato sitk
# es el paciente_sitk pero en un array para su impresion por pa pantalla de la aplicacion
paciente_array = None
nodulo_sitk = None  # Mascara del nodulo cancerigeno en sitk
pulmones_sitk = None  # Imagen con los pulmones segementados en sitk
pulmones_array = None
ws_sitk = None  # Imagen con las diferentes regiones etiquetadas
nodulo_segmentado = None  # Imagen con solo el nódulo en sitk
nodulo_segmentado_array = None
nodulo_overlay = None
region_cancer = None  # la etiqueta de la región que contiene el cáncer en el watershed
representado = None
direcciones_de_pacientes = ["./QIN LUNG CT/QIN-LSC-0003/04-01-2015-1-CT Thorax wContrast-41946/",
                            "./QIN LUNG CT/QIN-LSC-0014/11-06-2014-1-CT Thorax wContrast-34336/",
                            "./QIN LUNG CT/QIN-LSC-0028/11-06-2014-1-CT Thorax wContrast-24475/",
                            "./QIN LUNG CT/QIN-LSC-0049/11-06-2014-1-CT Thorax wContrast-14304/",
                            "./QIN LUNG CT/QIN-LSC-0064/11-06-2014-1-CT Thorax wContrast-93556/",
                            "./QIN LUNG CT/QIN-LSC-0088/11-06-2014-1-CT Thorax wContrast-43458/",
                            "./QIN LUNG CT/QIN-LUNG-01-0007/11-06-2014-1-CT Thorax wContrast-47252/",
                            "./QIN LUNG CT/QIN-LUNG-01-0013/04-01-2015-1-CT Thorax wContrast-97602/"]


def escoge_paciente(paciente):
    dir = lectura.busca_carpetas(direcciones_de_pacientes[paciente])

    return [direcciones_de_pacientes[paciente] + "/" + nombre for nombre in dir]


def leer_directorio_usuario(direc_paciente):
    """directorio_paciente es una String con la ruta a la carpeta principal del 
    paciente QIN... Modifica las variables globales de paciente_sitk"""
    global paciente_sitk, paciente_array, nodulo_sitk
    paciente_sitk, nodulo_sitk = lectura.leer_paciente(direc_paciente)
    paciente_array = funciones.obtener_array(paciente_sitk)
    # La funcion leer paciente devuelve una lista de nodulos y solo cogemos uno de ellos
    nodulo_sitk = nodulo_sitk[0]
    nodulo_sitk = sitk.GetImageFromArray(nodulo_sitk)
    nodulo_sitk.CopyInformation(paciente_sitk)
    nodulo_sitk = sitk.Cast(nodulo_sitk, sitk.sitkUInt32)





def segmentacion_pulmones(paciente_sitk, semillas):
    """Modifica la variable global pulmones_sitk. """
    global pulmones_sitk, pulmones_array
    pulmones_sitk = funciones.lung_segmentation(paciente_sitk, semillas)
    pulmones_array = funciones.obtener_array(pulmones_sitk)
    


def realizar_watershed(pulmones_sitk, nivel=29):
    """Modifica la variable global ws_sitk"""
    global ws_sitk
    ws_sitk = sitk.MorphologicalWatershed(sitk.GradientMagnitude(
        pulmones_sitk), markWatershedLine=True, level=nivel)
    


def extraer_caracteristicas_nodulo(etiqueta_candidato):
    """Devuelve una tupla con la (elongacion, energia, roudness, tamaño) """
    # Creamos el extractor de caracteristicas
    extractor = rad.featureextractor.RadiomicsFeatureExtractor()
    extractor.disableAllFeatures()
    extractor.enableFeaturesByName(glcm=["JointEnergy"], shape=[
                                   'Sphericity', 'Elongation'])

    result = extractor.execute(paciente_sitk, ws_sitk, etiqueta_candidato)

    sphericity = result['original_shape_Sphericity']
    elongation = result['original_shape_Elongation']
    energy = result['original_glcm_JointEnergy']

    return (elongation, energy, sphericity)


def obtener_mascara():
    global nodulo_segmentado, ws_sitk, region_cancer, nodulo_segmentado_array
    nodulo_segmentado = experimentacion.extraer_mascara(ws_sitk, region_cancer)
    nodulo_segmentado_array = funciones.obtener_array(nodulo_segmentado)


def extraer_etiqueta():
    """devuelve la etiqueta de la region en la que se encuentra el nodulo cancerigeno"""
    global region_cancer, ws_sitk, nodulo_sitk, pulmones_sitk
    region_cancer = experimentacion.comprobar_existencia_nodulo(
        ws_sitk, nodulo_sitk, pulmones_sitk)
    obtener_mascara()
    


def devuelve_array(slice):
    """Devuelve un array de numpy de dos dimensiones """
    return representado[:, :, slice]
