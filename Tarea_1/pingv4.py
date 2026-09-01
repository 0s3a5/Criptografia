import sys
import time
import struct
from scapy.all import IP, ICMP, send

if len(sys.argv) != 2:
    print("Uso: python3 pingv4.py \"texto_cifrado\"")
    sys.exit(1)

texto_cifrado = sys.argv[1]
ip_dest = "127.0.0.1"  
ip_id = 1000
seq_num = 1
icmp_id = 1234

for char in texto_cifrado:
    # 1. Obtenemos el tiempo actual en segundos y lo empaquetamos en 8 bytes (little-endian)
    # Esto genera un timestamp real para mantener la coherencia temporal.
    timestamp_real = struct.pack("<Q", int(time.time()))
   
    # 2. Desarmamos y rearmamos los primeros 8 bytes (el bloque del timestamp)
    char_byte = char.encode('utf-8')       # Byte 0: El caracter cifrado
    timestamp_2_bytes = timestamp_real[1:3] # Bytes 1 y 2: Conservamos parte del timestamp real
    cinco_ceros = b'\x00\x00\x00\x00\x00'  # Bytes 3 al 7: 5 ceros exigidos por la rúbrica
   
    # 3. El padding clásico del ping en Linux (40 bytes, desde 0x10 hasta 0x37)
    payload_padding = bytes(range(0x10, 0x38))
   
    # Ensamblamos los 48 bytes exactos del payload
    data = char_byte + timestamp_2_bytes + cinco_ceros + payload_padding

    # Crear el paquete. Al no declarar el checksum manual, Scapy lo calcula de manera coherente.
    pkt = IP(dst=ip_dest, id=ip_id) / ICMP(id=icmp_id, seq=seq_num) / data
   
    send(pkt, verbose=False)
    print(f"Sent 1 packets.")
   
    # Incrementamos los contadores para mantener la coherencia de secuencia e identificación
    ip_id += 1
    seq_num += 1
   
    # Mantiene la ejecución cíclica para no saturar y pasar desapercibido
    time.sleep(1)
