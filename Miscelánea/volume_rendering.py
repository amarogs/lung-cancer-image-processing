import numpy as np
import vtk as vtk
import SimpleITK as sitk
import funciones
from itkwidgets import view
import itk as itk
from vtk.util import numpy_support


def create_volume(sitk_image):
 
    image = sitk.GetArrayFromImage(sitk_image)
    # The volume will be displayed by ray-cast alpha compositing.
    # A ray-cast mapper is needed to do the ray-casting.
    data_importer = vtk.vtkImageImport()
 
    data_string = image.tostring()
    
    data_importer.CopyImportVoidPointer(data_string, len(data_string))
    volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputConnection(data_importer.GetOutputPort())
    
    # The color transfer function maps voxel intensities to colors.
    # It is modality-specific, and often anatomy-specific as well.
    # The goal is to one color for flesh (between 500 and 1000)
    # and another color for bone (1150 and over).
    volumeColor = vtk.vtkColorTransferFunction()
    
    volumeColor.AddRGBPoint(-1000, 1.0, 0.5, 0.3)
    volumeColor.AddRGBPoint(-200, 1.0, 0.5, 0.3)
    

    # The opacity transfer function is used to control the opacity
    # of different tissue types.
    volumeScalarOpacity = vtk.vtkPiecewiseFunction()
    
    volumeScalarOpacity.AddPoint(-1000, 0.15)
    volumeScalarOpacity.AddPoint(-200, 0.15)
    

    # The gradient opacity function is used to decrease the opacity
    # in the "flat" regions of the volume while maintaining the opacity
    # at the boundaries between tissue types.  The gradient is measured
    # as the amount by which the intensity changes over unit distance.
    # For most medical data, the unit distance is 1mm.

    volumeGradientOpacity = vtk.vtkPiecewiseFunction()
    volumeGradientOpacity.AddPoint(0, 0.0)
    volumeGradientOpacity.AddPoint(90, 0.5)
    volumeGradientOpacity.AddPoint(100, 1.0)

    # The VolumeProperty attaches the color and opacity functions to the
    # volume, and sets other volume properties.  The interpolation should
    # be set to linear to do a high-quality rendering.  The ShadeOn option
    # turns on directional lighting, which will usually enhance the
    # appearance of the volume and make it look more "3D".  However,
    # the quality of the shading depends on how accurately the gradient
    # of the volume can be calculated, and for noisy data the gradient
    # estimation will be very poor.  The impact of the shading can be
    # decreased by increasing the Ambient coefficient while decreasing
    # the Diffuse and Specular coefficient.  To increase the impact
    # of shading, decrease the Ambient and increase the Diffuse and Specular.
    volumeProperty = vtk.vtkVolumeProperty()
    #volumeProperty.SetColor(volumeColor)
    #volumeProperty.SetScalarOpacity(volumeScalarOpacity)
   # volumeProperty.SetGradientOpacity(volumeGradientOpacity)
    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.ShadeOn()
    volumeProperty.SetAmbient(0.4)
    volumeProperty.SetDiffuse(0.6)
    volumeProperty.SetSpecular(0.2)

    # The vtkVolume is a vtkProp3D (like a vtkActor) and controls the position
    # and orientation of the volume in world coordinates.
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
   # volume.SetProperty(volumeProperty)

def show_actor(actor):

    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size

    ren.AddActor(actor)
    renWin.SetSize(500, 500)
    renWin.SetWindowName('CT-scan')


    renWin.SetMultiSamples(4)

    # This allows the interactor to initalize itself. It has to be
    # called before an event loop.
    iren.Initialize()

    # We'll zoom in a little by accessing the camera and invoking a "Zoom"
    # method on it.
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.5)
    renWin.Render()

    # Start the event loop.
    iren.Start()

    return 
def vtk_image_from(sitk_image):
    #We create the data we want to render. We create a 3D-image by a X-ray CT-scan made to an object. We store the values of each
    #slice and we complete the volume with them in the z axis
    spacing = sitk_image.GetSpacing()
    print(spacing)
    matrix_full = sitk.GetArrayFromImage(sitk_image).T
    matrix_full = np.array(np.swapaxes(matrix_full, 1, 2))

    # For VTK to be able to use the data, it must be stored as a VTK-image. This can be done by the vtkImageImport-class which
    # imports raw data and stores it.
    dataImporter = vtk.vtkImageImport()
    # The previously created array is converted to a string of chars and imported.
    data_string = matrix_full.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    # The type of the newly imported data is set to unsigned short (uint16)
    dataImporter.SetDataScalarTypeToUnsignedShort()
    dataImporter.SetDataSpacing(spacing[2], spacing[1], spacing[0])
    # Because the data that is imported only contains an intensity value (it isnt RGB-coded or someting similar), the importer
    # must be told this is the case.
    dataImporter.SetNumberOfScalarComponents(1)

    # The following two functions describe how the data is stored and the dimensions of the array it is stored in.
    w, h, d = matrix_full.shape
    print(w, h, d)

    dataImporter.SetDataExtent(0, h-1, 0, d-1, 0, w-1)
    dataImporter.SetWholeExtent(0, h-1, 0, d-1, 0, w-1)

    return dataImporter


def ver_superficie(dataImporter):

    voxelModeller = vtk.vtkVoxelModeller()
    voxelModeller.SetSampleDimensions(512, 512, 73)
    voxelModeller.SetInputConnection(dataImporter.GetOutputPort())

    surface = vtk.vtkMarchingCubes()
    surface.SetInputData(voxelModeller.GetOutput())
    surface.SetValue(0,180)
    surface.ComputeNormalsOn()
    

    ## mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(surface.GetOutputPort())
    ##actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

def crear_actor(dataImporter):
    """https://stackoverflow.com/questions/42345011/vtk-numpy-for-3d-image-rendering-and-visualization"""


    # This class stores color data and can create color tables from a few color points.
    colorFunc = vtk.vtkPiecewiseFunction()
    colorFunc.AddPoint(-1024, 0.0)
    colorFunc.AddPoint(0, 1)

    # The following class is used to store transparency-values for later retrieval.

    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    #Create transfer mapping scalar value to opacity
    alphaChannelFunc.AddPoint(-1024, 0.0)
    alphaChannelFunc.AddPoint(0, 1)


    # The gradient opacity function is used to decrease the opacity
    # in the "flat" regions of the volume while maintaining the opacity
    # at the boundaries between tissue types.  The gradient is measured
    # as the amount by which the intensity changes over unit distance.
    # For most medical data, the unit distance is 1mm.
    volumeGradientOpacity = vtk.vtkPiecewiseFunction()
    volumeGradientOpacity.AddPoint(-1024,   0.0)
    volumeGradientOpacity.AddPoint(-200,  0.5)
    volumeGradientOpacity.AddPoint(3000, 1.0)

    # The previous two classes stored properties. Because we want to apply these properties to the volume we want to render,
    # we have to store them in a class that stores volume properties.
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorFunc)
    volumeProperty.SetScalarOpacity(alphaChannelFunc)
    volumeProperty.SetGradientOpacity(volumeGradientOpacity)


    volumeProperty.SetInterpolationTypeToLinear()

    #volumeProperty.ShadeOn();

    # This class describes how the volume is rendered (through ray tracing).
    
    # We can finally create our volume. We also have to specify the data for it, as well as how the data will be rendered.
    volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
    # function to reduce the spacing between each image
    #volumeMapper.SetMaximumImageSampleDistance(0.01)
    
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort())

    # The class vtkVolume is used to pair the previously declared volume as well as the properties to be used when rendering that volume.
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    return volume
 

img = funciones.leer_dicom("./database/0/")
dataImporter = vtk_image_from(img)

v = ver_superficie(dataImporter)
show_actor(v)
