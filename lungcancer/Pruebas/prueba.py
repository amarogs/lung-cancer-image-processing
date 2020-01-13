import lungcancer.Funciones.funciones as funciones
import lungcancer.Funciones.lectura as lectura
import SimpleITK as sitk

#Cargamos la imagen que deseamos leer
img = lectura.leer_dicom("./QIN LUNG CT/QIN-LSC-0003/04-01-2015-1-CT Thorax wContrast-41946/2-THORAX W  3.0  B41 Soft Tissue-71225")

funciones.mostrar_slice(img, 69)

#Cargamos la mascara del nodulo
img_nodulo = lectura.leer_una_imagen("./QIN LUNG CT/QIN-LSC-0003/04-01-2015-1-CT Thorax wContrast-41946/1000-QIN CT challenge alg01 run01segmentation")
img_nodulo = sitk.GetImageFromArray(img_nodulo)
img_nodulo.CopyInformation(img)

#Realizamos la segmentación
seeds = [(100, 250, 65), (350, 350, 65)]

img_segmentada = funciones.lung_segmentation(img, seeds)
funciones.mostrar_slice(img_segmentada, 69)
