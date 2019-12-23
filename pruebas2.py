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
img = funciones.leer_dicom(
    "./QIN LUNG CT/QIN-LSC-0003/04-01-2015-1-CT Thorax wContrast-41946/2-THORAX W  3.0  B41 Soft Tissue-71225")

img_nodulo = funciones.leer_una_imagen("./QIN LUNG CT/QIN-LSC-0003/04-01-2015-1-CT Thorax wContrast-41946/1000-QIN CT challenge alg01 run02segmentation result-72120")
img_nodulo = sitk.GetImageFromArray(img_nodulo)
img_nodulo.CopyInformation(img)

# funciones.mostrar_slice(img)

# Habría que meterlo con la aplicación
seeds = [(100, 250, 65 ),(350, 350, 65) ]
[img.GetPixel(s) for s in seeds]

img = funciones.lung_segmentation(img, seeds)
# count = np.sum(sitk.GetArrayFromImage(img_binaria))

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

def extraer_caracteristicas(img_sitk, img_ws, labels):

    #Creamos el extractor de caracteristicas
    extractor = rad.featureextractor.RadiomicsFeatureExtractor()
    extractor.disableAllFeatures()
    extractor.enableFeaturesByName(glcm=["JointEnergy"],shape=['Sphericity', 'Elongation'])

    #Por cada etiqueta obtenemos su valor
    results = []

    nombres = ["label", "sphericity", "elongation", "energy"]
    datos = []
    for label in labels:
            result = extractor.execute(img, img_ws, label=label)

            sphericity = result['original_shape_Sphericity']
            elongation = result['original_shape_Elongation']
            energy = result['original_glcm_JointEnergy']
            datos.append((label,sphericity, elongation, energy))

    print(pd.DataFrame(data=datos, columns=nombres))
    



def calcula_dimensiones(img, ws):
    lsif = sitk.LabelStatisticsImageFilter()
    lsif.Execute(img, ws)

    labels = []
    for i in lsif.GetLabels():
        
        boundingBox = np.array(lsif.GetBoundingBox(i))
        ndims = np.sum((boundingBox[1::2] - boundingBox[0::2] + 1) > 1)
        if ndims >= 3:
            labels.append(i)

    return labels

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


verts, faces = funciones.make_mesh(reg,-200)
funciones.plotly_3d(verts, faces,)

ruta = "./QIN LUNG CT/QIN-LSC-0003/04-01-2015-1-CT Thorax wContrast-41946/1000-QIN CT challenge alg02 run3segmentation result-58041/000000.dcm"
una_imagen = funciones.leer_una_imagen(ruta)
funciones.mostrar_slice(una_imagen)


info = pd.read_csv('./FeaturesWithLabels.csv')
