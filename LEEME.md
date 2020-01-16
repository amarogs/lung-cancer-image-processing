# lung-cancer-image-processing
Repositorio que contiene el código para el trabajo de la asignatura PID

Como la aplicación está escrita en Python 3, debemos tenerlo instalado en nuestro sistema. Para instalarlo en Windows o MacOS debemos descargarnos el instalador desde la web de Python: https://www.python.org/downloads/, en cambio si estamos sobre un sistema Debian podemos instalarlo con el instalador de paquetes apt realizando el siguiente comando: sudo apt-get install -y python3, además, una vez se haya completado la instalación debemos instalar el gestor de paquetes de Python 3: apt-get install -y pip3. 
El siguiente paso para poder ejecutar la aplicación consiste instalar los módulos necesarios, para ello debemos localizar la terminal de nuestro equipo y realizar los siguientes comandos: 

    pip3 install pydicom
    pip3 install SimpleITK
    pip3 install pyradiomics
    pip3 install numpy
    pip3 install matplotlib
    pip3 install plotly
    pip3 install scikit-image
    pip3 install PyQT5


Si nuestro sistema es Windows puede ocurrir que la referencia al instalador de paquetes de Python 3 se llame pip sin el 3, por tanto debemos eliminar en los anteriores comandos el 3. 
El comando pip/pip3 instala los paquetes para todos los usuarios del sistema, por tanto podemos tener problemas de gestión de permisos. Si esto ocurre debemos instalarlo únicamente para el usuario que hace el comando, esto se hace añadiendo --user al final de cada comando.

Una vez hayamos instalado todo el software necesario, para ejecutar la aplicación debemos irnos hasta la carpeta de Ejecutable y realizar el siguiente comando: python3 -m lungcancer.Aplicacion.app
