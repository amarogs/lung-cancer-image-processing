
directorio_paciente = None
paciente_sitk = None #DICOM del paciente en formato sitk
nodulo_sitk = None #Mascara del nodulo cancerigeno en sitk
pulmones_sitk = None #Imagen con los pulmones segementados en sitk
ws_sitk = None #Imagen con las diferentes regiones etiquetadas


def leer_directorio_usuario(directorio_paciente):
    """directorio_paciente es una String con la ruta a la carpeta principal del 
    paciente QIN... Modifica las variables globales de paciente_sitk y nodulo_sitk"""
    pass

def segmentacion_pulmones(paciente_sitk, semillas):
    """Modifica la variable global pulmones_sitk. """
    pass

def realizar_watershed(pulmones_sitk, nivel=29):
    """Modifica la variable global ws_sitk"""
    pass
def extraer_caracteristicas_nodulo():
    """Devuelve una tupla con la (elongacion, energia, roudness, tamaño) """
    pass