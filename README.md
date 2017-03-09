Transformer Deployer
========

##Instalación

1- Clonar el repositorio
 
`git clone git@github.com:BambuSolar/transformer_deployer.git`

2- Instalar dependencias

    sudo apt-get install python3
    sudo apt-get install python3-pip
    sudo apt-get install virtualenv python-virtualenv

3- Ejecutar el siguiente comando, solo en caso que el comando 5 falle

`export LC_ALL=C`

4- Cambiar al directorio donde se instaló el Transformer Deployer

`cd transformer_deployer`

5- Instalar en virtual environment

`virtualenv venv`

6- Activar en virtaul environment

`source venv/bin/activate`

7- Instalar las dependencias

`pip3 install -r requirements.txt`

8- Ejecutar el servidor

`python3 app/transformers_server.py`

##Configuración para ejecución en Producción

1- Instalamos la dependencia

`npm install forever -g`

2- Ejecutamos el servidor en modo background

`forever start -c python3 app/transformers_server.py`

3- Deterner el servidor en background

`forever stop -c python3 app/transformers_server.py`
