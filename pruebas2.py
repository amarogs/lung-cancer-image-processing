import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk
import pandas as pd
import funciones
import pydicom
import vtk
import volume_rendering

#Leemos la imagen en formato itk
img = funciones.leer_dicom("./database/0/")

#funciones.mostrar_slice(img_re)
funciones.mostrar_slice(img)

#Habría que meterlo con la aplicación
seeds = [(100, 250, 30 ),(350, 350, 30) ]
[img.GetPixel(s) for s in seeds]

img = funciones.lung_segmentation(img, seeds)
#count = np.sum(sitk.GetArrayFromImage(img_binaria))
#funciones.mostrar_slice(img_binaria)
funciones.mostrar_slice(img)

ws = sitk.MorphologicalWatershed(sitk.GradientMagnitude(img), markWatershedLine=True, level=7)
funciones.mostrar_slice(ws)

# stats = sitk.LabelShapeStatisticsImageFilter()
# stats.Execute(sitk.ConnectedComponent(ws))

# stats_list = [ (stats.GetPhysicalSize(i),
#                stats.GetElongation(i),
#                stats.GetFlatness(i),
#                stats.GetOrientedBoundingBoxSize(i)[0],
#                stats.GetOrientedBoundingBoxSize(i)[2]) for i in stats.GetLabels()]

# cols = ["Volume (nm^3)",
#         "Elongation",
#         "Flatness",
#         "Oriented Bounding Box Minimum Size(nm)",
#         "Oriented Bounding Box Maximum Size(nm)"]

# stats = pd.DataFrame(
#     data=stats_list, index=stats.GetLabels(), columns=cols)

# stats


#El thikness en este caso es 3 y spacing= 0,781
imgs_after_resamp, spacing = funciones.resample(
    img, [img.GetDimension()], [1, 1, 1])
img_arr = sitk.GetArrayFromImage(img)
v, f = funciones.make_mesh(img_arr, 350)
funciones.plt_3d(v, f)
