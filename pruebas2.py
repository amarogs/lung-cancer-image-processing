import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk
import funciones
import pydicom

#Leemos la imagen en formato itk
img = funciones.leer_dicom("./database/0/")

#La reconvertimos
img_re = sitk.RescaleIntensity(img, -1024, 3071)
funciones.mostrar_slice(img_re)


seeds = [(100, 250, 30 ),(350, 350, 30) ]
[img_re.GetPixel(s) for s in seeds]

img_binaria = funciones.lung_segmentation(img_re, seeds)
count = np.sum(sitk.GetArrayFromImage(img_binaria))
funciones.mostrar_slice(img_binaria)
