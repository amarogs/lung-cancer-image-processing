import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt

def get_image_from_slices(slices):
    """Dada una lista de slices devuleve un array n-dimensional de numpy
    que forma la imagen en 3D. 
    Código parcial de: link a la guia de pydicom.
    """

    # create 3D array
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)

    # fill 3D array with the images from the files
    for i, s in enumerate(slices):
        img2d = s.pixel_array
        img3d[:, :, i] = img2d
    return img3d

def get_pixels_hu(slices):
    """Código obtenido de: https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/ 
    Recibe un conjunto de slices de PyDicom y devuelve un array de numpy ndimensional."""
    #Create a 3D numpy array.
    image = get_image_from_slices(slices)

    # Convert to int16 (from sometimes int16),
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 1
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0
    
    # Convert to Hounsfield units (HU)
    intercept = slices[0].RescaleIntercept
    slope = slices[0].RescaleSlope
    
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
    for i in range(image.shape[2]):
        image[:, :, i] = image[:, :, i] + np.int16(intercept)
    
    
    return image


def lung_segmentation(imagen_hu, s1, s2):
    """Este método recibe una array N-dimensional con valores de intensidad en 
    escala HU (imagen) y dos puntos (x,y,z) que son las semillas del crecimiento de regiones"""
    #Transformamos la imagen N-dimensional a una imagen de ITK.
    img = sitk.GetImageFromArray(imagen_hu)

    #Aplicamos el filtro de suavizado Curvature Flow
    img = sitk.CurvatureFlow(image1=img, timeStep=0.125,numberOfIterations=5)

    #Obtenemos el crecimiento de regiones partiendo de s1, s2.
    #El resultado es una imagen binarizada.
    img = sitk.ConnectedThreshold(img,[s1,s2], lower=-1000, upper=-200)

    #Realizamos un cierre morfológico para unir pequeñas regiones separadas
    #img = sitk.BinaryMorphologicalClosing(img, 12, kenerl=)

    #Devolvemos la imagen como array N-dimensional
    return sitk.GetArrayFromImage(img)
