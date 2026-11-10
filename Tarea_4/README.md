En este apartado se encuentran los archivos que se utilizan en el informe de la tarea 4.
Se incluyen el Dockerfile y el sshd_config de la Actividad 1, y el script descifrar_transacciones.py de la Actividad 2.
Tambien se incluye la captura de wireshark de la conexion SSH
La captura transacciones_cifradas.pcap y la clave privada RSA son las que entrega el drive, se descargan desde el Drive del enunciado: https://drive.google.com/drive/folders/1rXMp5y9WeBR36iytc4RBaqXKWf3ea-WU

Tambien se incluye el pdf del informe
Y como ultimo se incluye el latex del informe

Actividad 1 
Para realizar la prueba se deben descargar el Dockerfile y el sshd_config y dejarlos en la misma carpeta
Una vez en la carpeta se debe de escribir los siguientes comandos en la terminal

1. sudo docker build -t ssh-lab4 .
#construye la imagen con el servidor SSH ya configurado
2. sudo docker run -d --name servidor-ssh-lab4 -p 2222:22 ssh-lab4
#levanta el contenedor, el servidor queda accesible en el puerto 2222
3. ssh -v -p 2222 estudiante@localhost
#la contraseña del usuario es cripto2026
#una vez adentro se puede escribir whoami, hostname y exit para salir

para ver el trafico en wireshark es necesario iniciar la captura en la interfaz loopback (lo) antes del paso 3
y luego filtrar por: ssh && tcp.port == 2222
si se quiere solo ver los resultados se puede abrir el archivo captura_ssh.pcapng

Para detener y borrar el contenedor al terminar
sudo docker stop servidor-ssh-lab4
sudo docker rm servidor-ssh-lab4

Actividad 2 

Para realizar la prueba se deben descargar el script, la captura y la clave y dejarlos en la misma carpeta
Una vez en la carpeta se debe de escribir los siguientes comandos en la terminal

python3 descifrar_transacciones.py transacciones_cifradas.pcap clave_privada.pem
   
si todo sale bien se debe ver el PIN 4827, 40 transacciones y al final el mensaje
40/40 transacciones descifradas y autenticadas correctamente

si se usa otra captura o otra clave se debe escribir el nombre de los archivos nuevos entre el script y los parametros

Es necesario destacar que todo lo hice en la distribucion de kali, en un entorno virtual de python (venv)
Si no se tiene docker se debe instalar con
sudo apt install -y docker.io
Si es otra distribucion o falta alguna libreria para el script se debe de utilizar
pip install scapy cryptography
