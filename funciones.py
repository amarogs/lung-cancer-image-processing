import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt



def lung_segmentation(img_original, seedList):
    """Este método recibe una array N-dimensional con valores de intensidad en 
    escala HU (imagen) y dos puntos (x,y,z) que son las semillas del crecimiento de regiones"""

    # Aplicamos el filtro de suavizado Curvature Flow
    img = sitk.CurvatureFlow(image1=img_original, timeStep=0.125, numberOfIterations=5)

    # Obtenemos el crecimiento de regiones partiendo de la lista de semillas
    # El resultado es una imagen binarizada.
    img = sitk.ConnectedThreshold(img, seedList, lower=-1000.0, upper=-200.0)

    # Realizamos un cierre morfológico para unir pequeñas regiones separadas
    img = sitk.BinaryMorphologicalClosing(img, 12, sitk.sitkBall)

    #Convertimos la imagen binaria en el mismo tipo que la imagen original
    img= sitk.Cast(img, sitk.sitkInt16)

    #Como dentro de la escala HU etá incluido el 0, vamos a sumar 1024 para que al multiplicar, el menor valor de la nueva
    #escala sea 0
    img_original = img_original + 1024

    #Realizamos la segmentación de los pulmones
    img_segmentada = sitk.Multiply(img,img_original)

    #Reescalamos a HU
    img_segmentada= img_segmentada-1024

    # Devolvemos la imagen de los pulmones segmentados
    return img_segmentada

def leer_dicom(directorio):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(directorio)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    img_re = sitk.RescaleIntensity(image, -1024, 3071)

    return img_re

def mostrar_slice(image_sitk):
    img = sitk.GetArrayFromImage(image_sitk)
    print("El min {} el max {}".format(np.min(img), np.max(img)))
    print(img.shape)
    
    new_array = np.array(np.swapaxes(img, 0, 2))
    new_array = np.array(np.swapaxes(new_array, 0, 1))
    
    #plt.imshow(new_array[:, :, new_array.shape[2]//2], cmap="gray")
    plt.imshow(new_array[new_array.shape[0]//2, :, :], cmap="gray")
    
    plt.show()


def obtener_array(imagen_sitk):
    """Dada una imagen itk la transformamos a np array y colocamos
    las componentes de manera adecuada. """
    img = sitk.GetArrayFromImage(imagen_sitk)
    new_array = np.array(np.swapaxes(img, 0, 2))
    new_array = np.array(np.swapaxes(new_array, 0, 1))

    return new_array
