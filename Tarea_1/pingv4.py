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
    timestamp_real = struct.pack("<Q", int(time.time()))
    char_byte = char.encode('utf-8')       
    timestamp_2_bytes = timestamp_real
    cinco_ceros = b'\x00\x00\x00\x00\x00'  
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
