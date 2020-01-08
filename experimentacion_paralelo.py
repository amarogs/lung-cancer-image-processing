from experimentacion import *
import multiprocessing


#Creamos tantos procesos como cores disponibles
pool = multiprocessing.Pool(5)

#Creamos la lista con los argumentos que vamos a probar.
argumentos = [(i, carpeta, list(range(25, 70))) for (i, carpeta) in enumerate(listado_dir_imagenes)]

#A cada core le damos los datos de un paciente y realiza la búsqueda en paralelo.
results = pool.map(experimenta_paciente, argumentos)
print(results)
pickle.dump(results, open("niveles.p", "wb"))

