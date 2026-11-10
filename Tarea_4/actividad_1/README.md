Si vuelo a repetir lo mismo por falta de ideas 

Actividad 1

Para realizar la prueba se deben descargar el Dockerfile y el sshd_config y dejarlos en la misma carpeta Una vez en la carpeta se debe de escribir los siguientes comandos en la terminal

sudo docker build -t ssh-lab4 . #construye la imagen con el servidor SSH ya configurado
sudo docker run -d --name servidor-ssh-lab4 -p 2222:22 ssh-lab4 #levanta el contenedor, el servidor queda accesible en el puerto 2222
ssh -v -p 2222 estudiante@localhost #la contraseña del usuario es cripto2026 #una vez adentro se puede escribir whoami, hostname y exit para salir
para ver el trafico en wireshark es necesario iniciar la captura en la interfaz loopback (lo) antes del paso 3 y luego filtrar por: ssh && tcp.port == 2222 si se quiere solo ver los resultados se puede abrir el archivo captura_ssh.pcapng

Para detener y borrar el contenedor al terminar sudo docker stop servidor-ssh-lab4 sudo docker rm servidor-ssh-lab4
