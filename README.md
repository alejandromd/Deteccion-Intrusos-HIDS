## Detección de intrusos (HIDS)

Se ha desarrollado el sistema HIDS donde se hashean con
SHA-256 los archivos de un sistema de información indicado por el cliente. Estos hashes se
almacenan en una base de datos tipo clave-valor LMDB para poder gestionar los hashes
fácilmente y hacer que la comprobación y restauración de la integridad sea más
eficiente y escalable. El tiempo por el que se repite la comprobación de la integridad puede
ser indicada, por defecto será de 1 día.

Para la restauración de estos archivos, en caso de fallo de la integridad, se emplea un
fichero de backup donde podéis escoger la ubicación de esta. Se compara cada archivo
con su contraparte en el directorio de verificación. Si no coinciden, este se reemplaza en
el directorio de verificación y se registra en un log la fecha y hora de reemplazo.
Existirá un informe de reemplazos por cada mes que el sistema HIDS esté activo. Para
mantener la confidencialidad e integridad de las rutas de verificación y backup, se
cifrarán con el sistema simétrico Fernet.

### Manual de uso

Estas son las librerías necesarias para que el servicio funcione correctamente:
- cffi==1.16.0 : permite integrar código en C de forma segura
- cryptography==42.0.5 : ofrece herramientas para la seguridad criptográfica
- lmdb==1.4.1 : facilita el almacenamiento eficiente de grandes conjuntos de datos en
memoria
- pycparser==2.21 : 'pycparser' ayuda en el análisis de código en C dentro de Python

Instalar las dependencias con:

`pip install -r requirements.txt`

(Se recomienda usar un entorno virtual de python para aislar las dependencias del sistema:
python -m venv env)

 Lanzar aplicación con:

`python -m src.cli`

La interfaz de usuario es en la terminal y para realizar la verificación de integridad de un
sistema de archivos hay que seguir los siguientes pasos:

- Una vez ejecutado el servicio, pulsar '1' para especificar la ruta donde estan los
archivos a verificar(pasar ruta completa, no relativa)
- Especificar ruta de backup(ruta completa)
- Escribir contraseña
- Para cambiar el intervalo de comprobación hay que entrar en
Claymore/src/utils/config.py y modificar la variable ‘CHECK_INTERVAL’ por el tiempo
deseado.
A parte de ‘seconds’ se pueden poner más formatos de tiempo(Consultar
datetime.py del manual de python para más información).
- Para salir del servicio y así detenerlo pulsar '2'.
