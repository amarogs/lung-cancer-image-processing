import os as os
import radiomics as rad
import pandas as pd
from funciones import *


def busca_carpetas(direct):
    return [c for c in os.listdir(direct) if c[0] != "."]


def ver_caracteristicas(img_sitk, mascara, paciente):

    #Creamos el extractor de caracteristicas
    extractor = rad.featureextractor.RadiomicsFeatureExtractor()
    extractor.disableAllFeatures()
    extractor.enableFeaturesByName(glcm=["JointEnergy"], shape=[
                                   'Sphericity', 'Elongation'])

    #Extraemos las caracteristicas de la mascara
    
    result = extractor.execute(img_sitk, mascara, label=1)

    sphericity = result['original_shape_Sphericity']
    elongation = result['original_shape_Elongation']
    energy = result['original_glcm_JointEnergy']
    
    return (paciente,sphericity, elongation, energy)




dir_base = "./QIN LUNG CT"
carpeta_nodulo = "1000-QIN"

nombres = ["paciente","sphericity", "elongation", "energy"]
datos = []

for carpeta_paciente in busca_carpetas(dir_base):
    siguiente = dir_base + "/" + carpeta_paciente + \
        busca_carpetas(siguiente)[0]

    img_paciente = None
    img_nodulos = []
    for carpeta in busca_carpetas(siguiente):
        
        directorio = siguiente + "/" + carpeta

        if carpeta[0:len(carpeta_nodulo)+1] == carpeta_nodulo:
            img_nodulos.append(leer_una_imagen(directorio))
        else:
            img_paciente = leer_dicom(directorio)

    #Por cada imagen de nodulos, copiamos los metadatos del paciente
    img_nodulos = [sitk.GetImageFromArray(nodulo).CopyInformation(
        img_paciente) for nodulo in img_nodulos]

    for (i,nodulo) in enumerate(img_nodulos):
        datos.append(ver_caracteristicas(img_paciente,nodulo, i))


dataframe = pd.DataFrame(data=datos, columns=nombres)
dataframe.to_csv("./datos_pacientes.csv")
    