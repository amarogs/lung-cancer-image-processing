import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk
import funciones
import pydicom

#Leemos la imagen en formato itk
img = funciones.leer_dicom("./database/0/")

#funciones.mostrar_slice(img_re)

#Habría que meterlo con la aplicación
seeds = [(100, 250, 30 ),(350, 350, 30) ]
[img.GetPixel(s) for s in seeds]

img = funciones.lung_segmentation(img, seeds)
#count = np.sum(sitk.GetArrayFromImage(img_binaria))
#funciones.mostrar_slice(img_binaria)
funciones.mostrar_slice(img)