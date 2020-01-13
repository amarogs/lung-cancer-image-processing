import os as os
import radiomics as rad
import pandas as pd
import pickle
import numpy as np

import lungcancer.Funciones.funciones as funciones
import lungcancer.Funciones.lectura as lectura


"""Variables globales """

DIR_BASE = "./QIN LUNG CT"
CARPETA_NODULO = "1000-QIN"
semillas_experimentacion = [
    [(82, 285, 65), (388, 308, 65)],
    [(146, 260, 54), (355, 269, 54)],
    [(175, 162, 56), (380, 259, 56)],
    [(133, 182, 55), (360, 230, 55)],
    [(168, 167, 51), (385, 188, 51)],
    [(128, 292, 52), (384, 284, 52)],
    [(148, 209, 59), (373, 324, 59)],
    [(125, 289, 56), (413, 280, 56)]]

UMBRAL_ESFERICIDAD = 0.449939379
UMBRAL_ELONGACION = 0.456512305
UMBRAL_ENERGIA = 0.0031626

#Valores umbral para la exploración de watershed
UMBRAL_CUBRIMIENTO = 0.6
UMBRAL_EXTENSION = 1.10



def caracteristicas_nodulo(img_paciente, mascara,region ,id_paciente, id_prueba=-1):
    """Dada una imagen sitk del paciente y una máscara del nódulo se extraen las características
    estadísticas del nódulo. """
    print("Calculando las caracteristicas del nodulo")
    #Creamos el extractor de caracteristicas
    extractor = rad.featureextractor.RadiomicsFeatureExtractor()
    extractor.disableAllFeatures()
    extractor.enableFeaturesByName(glcm=["JointEnergy"], shape=[
                                   'Sphericity', 'Elongation'])

    #Extraemos las caracteristicas de la mascara
    
    result = extractor.execute(img_paciente, mascara, label=region)
    print("Caracteristicas calculadas")
    sphericity = result['original_shape_Sphericity']
    elongation = result['original_shape_Elongation']
    energy = result['original_glcm_JointEnergy']
    
    return (id_paciente,id_prueba,sphericity, elongation, energy)


def obtencion_tablas_datos_nodulo(listado_dir_imagenes, archivo_salida):
    """Recibe la imagen de un paciente y la lista de máscaras del nódulo para extraer datos
    estadisticos que se guardan en la lista global DATOS. """

    nombres = ["paciente", "prueba", "sphericity", "elongation", "energy"]
    datos = []

    for (id_paciente, carpeta_paciente) in enumerate(listado_dir_imagenes):
        img_paciente, lista_nodulos = lectura.leer_paciente(carpeta_paciente)

        for (id_prueba, nodulo) in enumerate(lista_nodulos):
            nodulo = sitk.GetImageFromArray(nodulo)
            nodulo.CopyInformation(img_paciente)
            datos.append(caracteristicas_nodulo(img_paciente,nodulo,1,id_paciente, id_prueba))
    

    dataframe = pd.DataFrame(data=datos, columns=nombres)
    dataframe.to_excel("./"+archivo_salida+".xls")


def comprueba_si_esta_cancer(nodulo, ws, regiones_aceptadas):

    pixeles_cancer = np.sum(sitk.GetArrayFromImage(nodulo))
    etiquetas_cancer = sitk.Mask(ws, nodulo, maskingValue=1)

    #Creamos un objeto estadistico de sitk
    lsif = sitk.LabelStatisticsImageFilter()
    lsif.Execute(nodulo, etiquetas_cancer)
    aceptamos_nivel = False

    for region in regiones_aceptadas:
        pixeles_region = lsif.GetCount(region)
        if pixeles_region/pixeles_cancer > 0.8:
            aceptamos_nivel = True
            break
    return (aceptamos_nivel, region)

def experimentacion_watershed(listado_dir_imagenes, niveles_ws):
    niveles_watershed = []

    for (id_paciente, carpeta_paciente) in enumerate(listado_dir_imagenes):
        print("-------------------------------------------------------------------------")
        print("Estamos leyendo el paciente {} ".format(id_paciente))
        img_paciente, lista_nodulos = lectura.leer_paciente(carpeta_paciente)
        semillas_paciente = semillas_experimentacion[id_paciente]
        segmentacion_pulmones = funciones.lung_segmentation(img_paciente, semillas_paciente)
        print("Comenzando la experimentación de watershed")
        
        for nivel in niveles_ws:
            print("Explorando nivel {}".format(nivel))
            ws = sitk.MorphologicalWatershed( segmentacion_pulmones, markWatershedLine=True, level=nivel)
            
            #Creamos un objeto estadistico de sitk
            lsif = sitk.LabelStatisticsImageFilter()
            lsif.Execute(segmentacion_pulmones, ws)

            #Por cada region de watershed
            regiones_aceptadas = []
            labels = list(lsif.GetLabels())[1:]
            for region in reversed(labels):
                    #Comprobamos si tiene mas que 3 dimensiones
                    boundingBox = np.array(lsif.GetBoundingBox(region))
                    ndims = np.sum((boundingBox[1::2] - boundingBox[0::2] + 1) > 1)
                    print(region)
                    if ndims >= 3:
                        caracteristicas = caracteristicas_nodulo(segmentacion_pulmones, ws, region, id_paciente)
                        esfericidad, elongacion, energia = caracteristicas[2], caracteristicas[3], caracteristicas[4]
                        if esfericidad > UMBRAL_ESFERICIDAD and elongacion > UMBRAL_ELONGACION and energia > UMBRAL_ENERGIA:
                            regiones_aceptadas.append(region)
            
            #Una vez que tenemos todas las regiones filtradas, comprobamos que no haya sobresegmentación
            if len(regiones_aceptadas) > 0 and len(regiones_aceptadas) < 7:
                (aceptamos_nivel, region) = comprueba_si_esta_cancer(lista_nodulos[0], ws, regiones_aceptadas)
  
            else:
                #No aceptamos la segmentacion
                aceptamos_nivel = False

            if aceptamos_nivel:
                print("Para el paciente {} el nivel de watershed {} funciona".format(id_paciente, nivel))
                
                break

        # print(seeds, [img_paciente.GetPixel(s) for s in seeds])
            

def comprobar_existencia_nodulo(ws, nodulo, segmentacion_pulmones):

    ws = sitk.Cast(ws, sitk.sitkUInt32)
    pixeles_cancer = np.sum(sitk.GetArrayFromImage(nodulo))
    
    #print("El cancer tiene {} voxeles ".format( pixeles_cancer))
    #Creamos un objeto que mida las caracteristicas
    #de las etiquetas de la segmentación
    estadisticas_ws = sitk.LabelStatisticsImageFilter()
    estadisticas_ws.Execute(segmentacion_pulmones, ws)

    #Creamos un objeto que mida las caracteristicas de 
    #las etiquetas del interior del nódulo.
    etiquetas_cancer = sitk.Multiply(ws, nodulo)
    estadisticas_cancer = sitk.LabelStatisticsImageFilter()
    estadisticas_cancer.Execute(nodulo, etiquetas_cancer)
    #print(estadisticas_cancer.GetLabels())

    for region in estadisticas_cancer.GetLabels():
        if region != 0:
            pixeles_region = estadisticas_cancer.GetCount(region)
            cubrimiento = pixeles_region/pixeles_cancer
            if cubrimiento > UMBRAL_CUBRIMIENTO:
                extension = estadisticas_ws.GetCount(region)
                
                # print("Una region {} cubre el cancer en un {}%. Tiene {} extensión".format(
                #     region, cubrimiento, extension))
                if extension <= UMBRAL_EXTENSION*pixeles_cancer:
                    return region


def obtencion_semilla_ws(nodulo):
    """Erosionar y dilatar (en menor cantidad que la erosion) el nodulo para hacer una semilla
    del método de watershed con markers.  """
    #Hemos reducido el nodulo
    semilla = sitk.GrayscaleErode(nodulo, 6)
    semilla = sitk.GrayscaleDilate(nodulo, 2)
    return semilla



def experimenta_paciente(args):
    """Dado una carpeta con los datos del paciente una lista de niveles, realiza esos
    niveles de watershed para devolver un conjunto con los niveles que han sido fructíferos.
    Esta función es el bucle más externo de experimentacion_watershed_2 """
    id_paciente, carpeta_paciente, niveles_ws = args

    #Obtenemos las imagenes DICOM del paciente y la lista de sus nodulos
    img_paciente, lista_nodulos = lectura.leer_paciente(carpeta_paciente)
    #Obtenemos las semillas para la segmentación de los pulmones y los segmentamos
    semillas_paciente = semillas_experimentacion[id_paciente]
    segmentacion_pulmones = funciones.lung_segmentation(img_paciente, semillas_paciente)

    #Creamos el gradiente de los pulmones segmentados
    gradiente = sitk.GradientMagnitude(segmentacion_pulmones)

    #Obtenemos el nodulo 0 del paciente
    
    nodulo = lista_nodulos[0]
    del lista_nodulos[1:]
    nodulo = sitk.GetImageFromArray(nodulo)
    nodulo.CopyInformation(img_paciente)
    nodulo = sitk.Cast(nodulo, sitk.sitkUInt32)

    #Creamos una conjunto de niveles para el paciente
    niveles_paciente = set()
    
    
    for nivel in niveles_ws:
        #Realizmos el watershed
        ws = sitk.MorphologicalWatershed(gradiente, markWatershedLine=True, level=nivel)
        #Obtenemos la region con más de un 60% del cancer y como mucho un 10% más grande
        region = comprobar_existencia_nodulo(ws, nodulo, segmentacion_pulmones)

        if region != None:
            niveles_paciente.add(nivel)
    print("Completado el paciente ", id_paciente)
    return niveles_paciente
def experimentacion_watershed_2(listado_dir_imagenes, niveles_ws):
    niveles_watershed = []
    niveles_por_paciente = {}
    for (id_paciente, carpeta_paciente) in enumerate(listado_dir_imagenes):
        
        print("-------------------------------------------------------------------------")
        print("Estamos leyendo el paciente {} ".format(id_paciente))
        img_paciente, lista_nodulos = lectura.leer_paciente(carpeta_paciente)
        semillas_paciente = semillas_experimentacion[id_paciente]
        segmentacion_pulmones = funciones.lung_segmentation(
            img_paciente, semillas_paciente)

        #Obtenemos el nodulo 0 del paciente
        nodulo = lista_nodulos[0]
        nodulo = sitk.GetImageFromArray(nodulo)
        nodulo.CopyInformation(img_paciente)
        nodulo = sitk.Cast(nodulo, sitk.sitkUInt32)  

        #Creamos una lista de niveles para el paciente
        niveles_por_paciente[id_paciente] = set()
        gradiente = sitk.GradientMagnitude(segmentacion_pulmones)
        print("Comenzando la experimentación de watershed")

        for nivel in niveles_ws:
            print("*************************************************************")
            print("Explorando nivel ", nivel)
            
            ws = sitk.MorphologicalWatershed(gradiente, markWatershedLine=True, level=nivel)
            # ws = sitk.MorphologicalWatershedFromMarkers(segmentacion_pulmones, obtencion_semilla_ws(nodulo))
            region = comprobar_existencia_nodulo(ws, nodulo, segmentacion_pulmones)
            
            if region != None:
                niveles_por_paciente[id_paciente].add(nivel)
                print("He encontrado un nivel {} que tiene el cancer en {}".format(nivel, region))
    pickle.dump(niveles_por_paciente, open("niveles.p", "wb"))
    return niveles_por_paciente


def extraer_mascara(ws, region):
    ws_array = sitk.GetArrayFromImage(ws)

    mask = (1/region)*(ws_array == region)

    return sitk.GetImageFromArray(mask)


def extraer_region_interes(segmentacion_pulmones, nodulo, nivel, id_paciente):

    #Obtenemos el nodulo 0 del paciente
    nodulo = sitk.Cast(nodulo, sitk.sitkUInt32)
    #Realizamos ws
    ws = sitk.MorphologicalWatershed(sitk.GradientMagnitude(segmentacion_pulmones), markWatershedLine=True, level=nivel)
    #Obtenemos la region con más de un 60% del cancer y como mucho un 10% más grande
    region = comprobar_existencia_nodulo(ws, nodulo, segmentacion_pulmones)
    
    print("He encontrado una region {} ".format(region))
    caracteristicas = caracteristicas_nodulo(segmentacion_pulmones, ws, region, id_paciente)

    esfericidad, elongacion, energia = caracteristicas[2], caracteristicas[3], caracteristicas[4]
    if esfericidad > UMBRAL_ESFERICIDAD and elongacion > UMBRAL_ELONGACION and energia > UMBRAL_ENERGIA:
        print("La region {} cumple los criterios".format(region))
    else:
        print("La region {} no lo cumple".format(region))

def obtener_nivel_global(niveles_por_paciente):
    nivel = niveles_por_paciente[0]
    for i in range(1,len(niveles_por_paciente)):
        nivel = nivel.intersection(niveles_por_paciente[i])
    return nivel
def obtener_nivel_explicado():
    niveles = pickle.load(open("niveles.p", "rb"))
    niveles_no_vacios = []
    for (i, set_niveles) in enumerate(niveles):
        if len(set_niveles) == 0:
            print("No se han encontrado niveles para el paciente ", i)
        else:
            niveles_no_vacios.append(set_niveles)
    print("Los pacientes con niveles válidos de watershed tienen en común: {}".format(set.intersection(*niveles_no_vacios)))



  
