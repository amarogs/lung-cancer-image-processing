# lung-cancer-image-processing
Repositorio que contiene el código para el trabajo de la asignatura PID

Como la aplicación está escrita en Python 3, debemos tenerlo instalado en nuestro sistema. Para instalarlo en Windows o MacOS debemos descargarnos el instalador desde la web de Python: \href{https://www.python.org/downloads/}{Página de descargas}, en cambio si estamos sobre un sistema Debian podemos instalarlo con el instalador de paquetes apt realizando el siguiente comando: \emph{sudo apt-get install -y python3}, además, una vez se haya completado la instalación debemos instalar el gestor de paquetes de Python 3: \emph{apt-get install -y pip3}. 
El siguiente paso para poder ejecutar la aplicación consiste instalar los módulos necesarios, para ello debemos localizar la terminal de nuestro equipo y realizar los siguientes comandos: 
\begin{enumerate}
    \item pip3 install pydicom
    \item pip3 install SimpleITK
    \item pip3 install pyradiomics
    \item pip3 install numpy
    \item pip3 install matplotlib
    \item pip3 install plotly
    \item pip3 install scikit-image
    \item pip3 install PyQT5
\end{enumerate}

Si nuestro sistema es Windows puede ocurrir que la referencia al instalador de paquetes de Python 3 se llame pip sin el 3, por tanto debemos eliminar en los anteriores comandos el 3. 
El comando pip/pip3 instala los paquetes para todos los usuarios del sistema, por tanto podemos tener problemas de gestión de permisos. Si esto ocurre debemos instalarlo únicamente para el usuario que hace el comando, esto se hace añadiendo --user al final de cada comando.

Una vez hayamos instalado todo el software necesario, para ejecutar la aplicación debemos irnos hasta la carpeta de Ejecutable y realizar el siguiente comando: \emph{python3 -m lungcancer.Aplicacion.app}
