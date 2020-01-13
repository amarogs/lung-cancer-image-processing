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






def obtener_semilla_automatica(img):
    img_arr = sitk.GetArrayFromImage(img)
    new_array = np.array(np.swapaxes(img, 0, 2))
    new_array = np.array(np.swapaxes(new_array, 0, 1))
    X, Y, Z = new_array.shape
    seeds = []


    #Primera semilla
    x, y, z = (X//2, Y//5, Z//2)
    s = (x, y, z)

    valor = img.GetPixel(s)
    while valor > -200 or valor < -1024:
        s = (x, y+Y//20, z)
        valor = img.GetPixel(s)
    seeds.append(s)

    #Segunda semilla
    x, y, z= (x, 4*Y//5, Z//2)
    s = (x, y, z)

    valor = img.GetPixel(s)
    while valor > -200 or valor < -1024:
        s = (x, y-Y//20, z)
        valor = img.GetPixel(s)
    seeds.append(s)

    return seeds

def lung_segmentation(img_original, seedList):
    """Este método recibe una array N-dimensional con valores de intensidad en 
    escala HU (imagen) y dos puntos (x,y,z) que son las semillas del crecimiento de regiones"""

    # Aplicamos el filtro de suavizado gaussiano
    img = sitk.DiscreteGaussian(img_original, 10)
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

def mostrar_slice(image, n_slice=None):
    if  not isinstance(image, np.ndarray):
        img = sitk.GetArrayFromImage(image)
        new_array = np.array(np.swapaxes(img, 0, 2))
        new_array = np.array(np.swapaxes(new_array, 0, 1))

    else:
        new_array = image


    #Para encontrar el nodulo mostrar aquellas slices que tengan
    #un valor maximo mayor que 0

    if n_slice == None:
        n_slice = new_array.shape[2]//2
        
    plt.imshow(new_array[:, :, n_slice], cmap="gray")
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


def make_mesh(image, level=-650, step_size=1):
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


def myshow(img, title=None, margin=0.05, dpi=80):
    nda = sitk.GetArrayViewFromImage(img)
    spacing = img.GetSpacing()

    if nda.ndim == 3:
        # fastest dim, either component or x
        c = nda.shape[-1]

        # the the number of components is 3 or 4 consider it an RGB image
        if not c in (3, 4):
            nda = nda[nda.shape[0]//2, :, :]

    elif nda.ndim == 4:
        c = nda.shape[-1]

        if not c in (3, 4):
            raise Runtime("Unable to show 3D-vector Image")

        # take a z-slice
        nda = nda[nda.shape[0]//2, :, :, :]

    ysize = nda.shape[0]
    xsize = nda.shape[1]

    # Make a figure big enough to accommodate an axis of xpixels by ypixels
    # as well as the ticklabels, etc...
    figsize = (1 + margin) * ysize / dpi, (1 + margin) * xsize / dpi

    fig = plt.figure(figsize=figsize, dpi=dpi)
    # Make the axis the right size...
    ax = fig.add_axes([margin, margin, 1 - 2*margin, 1 - 2*margin])

    extent = (0, xsize*spacing[1], ysize*spacing[0], 0)

    t = ax.imshow(nda, extent=extent, interpolation=None)

    if nda.ndim == 2:
        t.set_cmap("gray")

    if(title):
        plt.title(title)

def overlay(pulmones_sitk, mascara_sitk, n_slice):
    pulmones_array = obtener_array(pulmones_sitk)
    mascara_array = obtener_array(mascara_sitk)

    plt.imshow(pulmones_array[:,:,n_slice], cmap="gray")
    plt.imshow(mascara_array[:, :, n_slice], cmap="Reds", alpha=0.5)

    plt.show()
