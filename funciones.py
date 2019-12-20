import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

import skimage
import pydicom as pydicom
import os
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.transform import resize


from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.tools import FigureFactory as FF
from plotly.graph_objs import *




def extraer_caracteristicas(img, img_ws):
    """Dada una imagen de sitk y su segmentación de watershed, extrae cada una de las  """

    img_arr = sitk.GetArrayFromImage(img)
    ws_arr = sitk.GetArrayFromImage(img_ws)

    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(img_ws)

    for label in stats.GetLabels():
        roundness = stats.GetRoundness(label)
        if roundness < 8.3*(10**4):
            elongation = stats.GetElongation(label)
            if elongation < 6.8*(10**4):
                region = extraer_etiqueta(img_arr, ws_arr, label)
                energy = calcular_energia(region)


def extraer_etiqueta(img, img_ws, label):
    """Recibe la imagen original como array, la imagen de watershed como array y 
    una etiqueta para extraer esa región de watershed de la imagen """

    mask = (1/label)*(img_ws == label)
    img = img + 1024
    img = img*mask
    img = img - 1024

    return img



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

def leer_una_imagen(directorio):
    """Dada el directorio de una imagen, la carga como imagen de numpy """

    files = []
    for fname in os.listdir(directorio):

        if fname[-3::] == "dcm":
            files.append(pydicom.read_file(directorio+"/"+fname))

    return files[0].pixel_array

def leer_dicom(directorio):
    """Dado un directorio, lee toda la serie dicom de un TAC """
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(directorio)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    img_re = sitk.RescaleIntensity(image, -1024, 3071)

    return img_re

def mostrar_slice(image):
    if  not isinstance(image, np.ndarray):
        img = sitk.GetArrayFromImage(image)
    else:
        img = image

    print("El min {} el max {}".format(np.min(img), np.max(img)))
    print(img.shape)
    
    new_array = np.array(np.swapaxes(img, 0, 2))
    new_array = np.array(np.swapaxes(new_array, 0, 1))
    
    plt.imshow(new_array[:, :, new_array.shape[2]//2], cmap="gray")
    #plt.imshow(new_array[new_array.shape[0]//2, :, :], cmap="gray")
    
    plt.show()


def obtener_array(imagen_sitk):
    """Dada una imagen itk la transformamos a np array y colocamos
    las componentes de manera adecuada. """
    img = sitk.GetArrayFromImage(imagen_sitk)
    new_array = np.array(np.swapaxes(img, 0, 2))
    new_array = np.array(np.swapaxes(new_array, 0, 1))

    return new_array

#De aqui hacia abajotodo lo nuevo para dibujar



def resample(image, dim,  new_spacing=[1, 1, 1]):
    # Determine current pixel spacing
    spac = list(image.GetSpacing()[:2])
    spacing = map(float, (dim + spac))
    spacing = np.array(list(spacing))

    img_arr = sitk.GetArrayFromImage(image)
    resize_factor = spacing / new_spacing
    new_real_shape = img_arr.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / img_arr.shape
    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(img_arr, real_resize_factor)

    return image, new_spacing


def make_mesh(image, level=None, step_size=1):
    print("Transposing surface")
    p = image.transpose(2, 1, 0)

    print("Calculating surface")
    verts, faces, norm, val = measure.marching_cubes_lewiner(
        p, level, step_size=step_size, allow_degenerate=True)
    return verts, faces


def plotly_3d(verts, faces):
    x, y, z = zip(*verts)

    print("Drawing")

    # Make the colormap single color since the axes are positional not intensity.
    #    colormap=['rgb(255,105,180)','rgb(255,255,51)','rgb(0,191,255)']
    colormap = ['rgb(236, 236, 212)', 'rgb(236, 236, 212)']

    fig = FF.create_trisurf(x=x,
                            y=y,
                            z=z,
                            plot_edges=False,
                            colormap=colormap,
                            simplices=faces,
                            backgroundcolor='rgb(64, 64, 64)',
                            title="Interactive Visualization")
    iplot(fig)


def plt_3d(verts, faces):
    print("Drawing")
    x, y, z = zip(*verts)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Fancy indexing: `verts[faces]` to generate a collection of triangles
    mesh = Poly3DCollection(verts[faces], linewidths=0.05, alpha=1)
    face_color = [1, 1, 0.9]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, max(x))
    ax.set_ylim(0, max(y))
    ax.set_zlim(0, max(z))
    ax.set_facecolor((0.7, 0.7, 0.7))
    plt.show()



