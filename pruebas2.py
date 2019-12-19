import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk
import pandas as pd
import funciones
import pydicom
import radiomics as rad
import six as six
import copy as copy
#Leemos la imagen en formato itk
img = funciones.leer_dicom("./database/0/")

# funciones.mostrar_slice(img_re)
# funciones.mostrar_slice(img)

# Habría que meterlo con la aplicación
seeds = [(100, 250, 30 ),(350, 350, 30) ]
[img.GetPixel(s) for s in seeds]

img = funciones.lung_segmentation(img, seeds)
# count = np.sum(sitk.GetArrayFromImage(img_binaria))
# funciones.mostrar_slice(img_binaria)
# funciones.mostrar_slice(img)

ws = sitk.MorphologicalWatershed(img, markWatershedLine=True, level=20, fullyConnected=False)
# funciones.mostrar_slice(ws)

def contar_voxels_por_etiqueta(img_ws):
    ws_array = sitk.GetArrayFromImage(img_ws)
    total_labels = np.max(ws_array)
    count_labels = {k:0 for k in range(total_labels+1)}

    for i in ws_array.flatten():
        count_labels[i]  = count_labels[i] + 1
    
    return count_labels

def extraer_energia(img_sitk, img_ws, labels):
    

    #Creamos el extractor de caracteristicas
    extractor = rad.featureextractor.RadiomicsFeatureExtractor()
    extractor.disableAllFeatures()
    extractor.enableFeaturesByName(glcm=['JointEnergy'])

    #Por cada etiqueta obtenemos su valor
    results = []

    #Quitamos la etiqueta 0 que esta reservada para el fondo de la imagen.
    
    
    for (label, count) in labels.items():
        if count > 10:
            result = extractor.execute(img, ws, label=label)
            results.append((label, result['original_glcm_JointEnergy']**0.5))

    return results



def calcula_dimensiones(img, ws):
    lsif = sitk.LabelStatisticsImageFilter()
    lsif.Execute(img, ws)

    dims = []
    for i in lsif.GetLabels():
        
        boundingBox = np.array(lsif.GetBoundingBox(i))
        ndims = np.sum((boundingBox[1::2] - boundingBox[0::2] + 1) > 1)
        dims.append(ndims)

    dims = np.array(dims)

    
    return np.sum((dims < 3))

def prueba_dimensiones(img):
    level = 10
    ws = sitk.MorphologicalWatershed(img, level=level, fullyConnected=False)
    ndims_menores = calcula_dimensiones(img, ws)

    while ndims_menores != 0:
        if level % 10 ==0:

            print("Explorando {} ndim: {}".format(level, ndims_menores))
        level += 1
        ws = sitk.MorphologicalWatershed(img, level=level)
        ndims_menores = calcula_dimensiones(img, ws)
        
    print(level)


reg = funciones.extraer_etiqueta(sitk.GetArrayFromImage(img), sitk.GetArrayFromImage(ws),1)
funciones.mostrar_slice(sitk.GetImageFromArray(reg))


verts, faces = funciones.make_mesh(reg, -900)
funciones.plotly_3d(verts, faces)