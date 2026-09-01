import sys
from scapy.all import rdpcap, ICMP

if len(sys.argv) != 2:
    print("Uso: python3 readv2.py <archivo.pcapng>")
    sys.exit(1)

pcap_file = sys.argv[1]
try:
    paquetes = rdpcap(pcap_file)
except Exception as e:
    print(f"Error al leer el archivo pcap: {e}")
    sys.exit(1)

texto_extraido = ""

# Lectura de pcap y extracción del payload
for pkt in paquetes:
    if pkt.haslayer(ICMP) and pkt[ICMP].type == 8:  # 8 = Echo Request
        try:
            payload = bytes(pkt[ICMP].payload)
            if len(payload) > 0:
                texto_extraido += chr(payload[0])
        except:
            pass

print(f"Texto cifrado extraído: {texto_extraido}\n")

# Mostrar todas las opciones de descifrado (Fuerza bruta de 1 a 26)
for i in range(1, 27):
    descifrado = ""
    for char in texto_extraido:
        if char.isalpha():
            ascii_base = ord('a') if char.islower() else ord('A')
            # Aplicar desplazamiento inverso
            descifrado += chr((ord(char) - ascii_base - i) % 26 + ascii_base)
        else:
            descifrado += char
           
    # Destaca en verde texto plano y llave si detecta una palabra clave
    if "criptografia" in descifrado.lower():
        print(f"\033[92m{descifrado}\n{i}\033[0m\n")
    else:
        print(f"{descifrado}\n{i}\n")
