import radiomics as rad
import experimentacion
import funciones
import SimpleITK as sitk
import numpy as np

directorio_paciente = None
paciente_sitk = None #DICOM del paciente en formato sitk
paciente_array = None #es el paciente_sitk pero en un array para su impresion por pa pantalla de la aplicacion
nodulo_sitk = None #Mascara del nodulo cancerigeno en sitk
pulmones_sitk = None #Imagen con los pulmones segementados en sitk
ws_sitk = None #Imagen con las diferentes regiones etiquetadas
region_cancer = None
direcciones_de_pacientes = ["./QIN LUNG CT/QIN-LSC-0003/04-01-2015-1-CT Thorax wContrast-41946/",
                            "./QIN LUNG CT/QIN-LSC-0014/11-06-2014-1-CT Thorax wContrast-34336/2-THORAX W  3.0  B41 Soft Tissue-85906",
                            "./QIN LUNG CT/QIN-LSC-0028/11-06-2014-1-CT Thorax wContrast-24475/2-THORAXW 3.0 B41 Soft Tissue-16822",
                            "./QIN LUNG CT/QIN-LSC-0049/11-06-2014-1-CT Thorax wContrast-14304/2-THORAX W  3.0  B41 Soft Tissue-57047",
                            "./QIN LUNG CT/QIN-LSC-0064/11-06-2014-1-CT Thorax wContrast-93556/2-THORAX W  3.0 B41 Soft Tissue-30421",
                            "./QIN LUNG CT/QIN-LSC-0088/11-06-2014-1-CT Thorax wContrast-43458/2-THORAXW  3.0  B40f-95200",
                            "./QIN LUNG CT/QIN-LUNG-01-0007/11-06-2014-1-CT Thorax wContrast-47252/2-THORAX W  3.0 B41 Soft Tissue-52055",
                            "./QIN LUNG CT/QIN-LUNG-01-0013/04-01-2015-1-CT Thorax wContrast-97602/2-THORAXW 3.0 B41 Soft Tissue-04801"]


def escoge_paciente(paciente):
    dir = experimentacion.busca_carpetas(direcciones_de_pacientes[paciente])

    return [ direcciones_de_pacientes[paciente] + "/" + nombre for nombre in dir]


def leer_directorio_usuario(direc_paciente):

    """directorio_paciente es una String con la ruta a la carpeta principal del 
    paciente QIN... Modifica las variables globales de paciente_sitk"""
    paciente_sitk, nodulo_sitk = experimentacion.leer_paciente(direc_paciente)
    paciente_array = funciones.obtener_array(paciente_sitk)
    nodulo_sitk = nodulo_sitk[0] #La funcion leer paciente devuelve una lista de nodulos y solo cogemos uno de ellos
    pass

def segmentacion_pulmones(paciente_sitk, semillas):
    """Modifica la variable global pulmones_sitk. """
    pulmones_sitk = funciones.lung_segmentation(paciente_sitk,semillas)
    pass

def realizar_watershed(pulmones_sitk, nivel=29):
    """Modifica la variable global ws_sitk"""
    ws_sitk = sitk.MorphologicalWatershed(pulmones_sitk, markWatershedLine=True, level=nivel)
    pass

def extraer_caracteristicas_nodulo(etiqueta_candidato):
    """Devuelve una tupla con la (elongacion, energia, roudness, tamaño) """
    # Creamos el extractor de caracteristicas

    extractor = rad.featureextractor.RadiomicsFeatureExtractor()
    extractor.disableAllFeatures()
    extractor.enableFeaturesByName(glcm=["JointEnergy"], shape=['Sphericity', 'Elongation','VoxelVolume'],)

    result = extractor.execute(paciente_sitk, ws_sitk, etiqueta_candidato)

    sphericity = result['original_shape_Sphericity']
    elongation = result['original_shape_Elongation']
    energy = result['original_glcm_JointEnergy']
    tamanio = result['original_shape_Volume']

    return (elongation, energy, sphericity,tamanio)

def extraer_etiqueta():
    """devuelve la etiqueta de la region en la que se encuentra el nodulo cancerigeno"""
    region_cancer = experimentacion.comprobar_existencia_nodulo(ws_sitk, nodulo_sitk, pulmones_sitk)
    pass

def devuelve_array(slice): #Fubcion que utilizamos para imprimir slices del DICOM, aquí solo las devolvemos

    if not isinstance(paciente_array, np.ndarray):
        img = sitk.GetArrayFromImage(paciente_array)
    else:
        img = paciente_array

    # Para encontrar el nodulo mostrar aquellas slices que tengan
    # un valor maximo mayor que 0
    new_array = np.array(np.swapaxes(img, 0, 2))
    new_array = np.array(np.swapaxes(new_array, 0, 1))

    if slice == None:
        slice = new_array.shape[2] // 2

    return new_array[:, :, slice]