import os as os
import radiomics as rad
import pandas as pd
from funciones import *


def busca_carpetas(direct):
    return [c for c in os.listdir(direct) if c[0] != "."]


def ver_caracteristicas(img_sitk, mascara, paciente, prueba):

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
    
    return (paciente,prueba,sphericity, elongation, energy)




dir_base = "./Lung Phantom"
carpeta_nodulo = "1000-QIN"

nombres = ["paciente","prueba","sphericity", "elongation", "energy"]
datos = []

for (paciente,carpeta_paciente) in enumerate( busca_carpetas(dir_base)):
    siguiente = dir_base + "/" + carpeta_paciente
    siguiente = siguiente + "/" + busca_carpetas(siguiente)[0]
    img_paciente = None
    img_nodulos = []
    for carpeta in busca_carpetas(siguiente):
        
        directorio = siguiente + "/" + carpeta
        if carpeta.startswith(carpeta_nodulo):
            img_nodulos.append(leer_una_imagen(directorio))
        else:
            img_paciente = leer_dicom(directorio)


    for (prueba,nodulo) in enumerate(img_nodulos):
        nodulo=sitk.GetImageFromArray(nodulo)
        nodulo.CopyInformation(img_paciente)
        datos.append(ver_caracteristicas(img_paciente,nodulo,paciente, prueba))


dataframe = pd.DataFrame(data=datos, columns=nombres)
dataframe.to_excel("./datos_pacientesLP.xls")
    