import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt



def lung_segmentation(img, seedList):
    """Este método recibe una array N-dimensional con valores de intensidad en 
    escala HU (imagen) y dos puntos (x,y,z) que son las semillas del crecimiento de regiones"""

    # Aplicamos el filtro de suavizado Curvature Flow
    img = sitk.CurvatureFlow(image1=img, timeStep=0.125, numberOfIterations=5)

    # Obtenemos el crecimiento de regiones partiendo de la lista de semillas
    # El resultado es una imagen binarizada.
    img = sitk.ConnectedThreshold(img, seedList, lower=-1000.0, upper=-200.0)

    # Realizamos un cierre morfológico para unir pequeñas regiones separadas
    img = sitk.BinaryMorphologicalClosing(img, 12, sitk.sitkBall)

    # Devolvemos la imagen como array N-dimensional
    return img


def prueba():
    """Este método recibe una array N-dimensional con valores de intensidad en 
    escala HU (imagen) y dos puntos (x,y,z) que son las semillas del crecimiento de regiones"""
    # Transformamos la imagen N-dimensional a una imagen de ITK.
    imagen_hu = np.zeros((9, 9, 5))
    imagen_hu[4:6, 4:6, 2:4] = 5

    img = sitk.GetImageFromArray(imagen_hu)

    # Aplicamos el filtro de suavizado Curvature Flow
    #img = sitk.CurvatureFlow(image1=img, timeStep=0.125, numberOfIterations=5)

    # Obtenemos el crecimiento de regiones partiendo de s1, s2.
    # El resultado es una imagen binarizada.

    img = sitk.ConnectedThreshold(img, [(2, 4, 4)], lower=4.0, upper=6.0)
    sitk.ConnectedThreshold()

    # Realizamos un cierre morfológico para unir pequeñas regiones separadas
    # img = sitk.BinaryMorphologicalClosing(img, 12, kenerl=)

    # Devolvemos la imagen como array N-dimensional
    return imagen_hu, sitk.GetArrayFromImage(img)


def leer_dicom(directorio):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(directorio)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()

    return image

def mostrar_slice(image_sitk):
    img = sitk.GetArrayFromImage(image_sitk)
    print("El min {} el max {}".format(np.min(img), np.max(img)))
    print(img.shape)
    
    new_array = np.array(np.swapaxes(img, 0, 2))
    new_array = np.array(np.swapaxes(new_array, 0, 1))
    
    print(new_array.shape)
    plt.imshow(new_array[:, :, new_array.shape[2]//2], cmap="gray")
    plt.show()
