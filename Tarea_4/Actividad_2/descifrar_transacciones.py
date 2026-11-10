#!/usr/bin/env python3
import sys
from scapy.all import rdpcap, TCP, Raw
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

pcap_path, key_path = sys.argv[1], sys.argv[2]

# 1. Leer payloads TCP guardando el numero de frame
payloads = []
for i, p in enumerate(rdpcap(pcap_path), 1):
    if p.haslayer(TCP) and p.haslayer(Raw):
        payloads.append((i, bytes(p[Raw].load)))

# 2. Paquete RSA_PIN: etiqueta + salt (16) + PIN cifrado (256)
frame, pkt = payloads[0]
assert pkt.startswith(b"RSA_PIN|")
body = pkt[len(b"RSA_PIN|"):]
salt, enc_pin = body[:16], body[16:16 + 256]
print(f"[+] Paquete RSA_PIN: frame #{frame} (payload de {len(pkt)} bytes)")
print(f"[+] Salt (16 bytes, hex): {salt.hex()}")
print(f"[+] PIN cifrado: {len(enc_pin)} bytes")

# 3. Recuperar el PIN con RSA-OAEP (SHA-256)
with open(key_path, "rb") as f:
    priv = serialization.load_pem_private_key(f.read(), password=None)
pin = priv.decrypt(enc_pin, padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(), label=None))
print("[+] PIN recuperado (RSA-OAEP/SHA-256):", pin.decode())

# 4. Derivar la clave AES-256 con Scrypt
key = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1).derive(pin)
print("[+] Clave AES-256 derivada con Scrypt (n=2^14, r=8, p=1):", key.hex())

# 5. Descifrar los paquetes AESGCM
aes = AESGCM(key)
tag_prefix = b"AESGCM|"
txs = [(f, p) for f, p in payloads if p.startswith(tag_prefix)]
print("[+] Paquetes AESGCM encontrados:", len(txs))
print("\n" + "=" * 30 + " TRANSACCIONES " + "=" * 30)

ok = 0
for n, (frame, p) in enumerate(txs, 1):
    data = p[len(tag_prefix):]
    nonce, ct_and_tag = data[:12], data[12:]
    try:
        msg = aes.decrypt(nonce, ct_and_tag, None)  # verifica el tag
        ok += 1
        print(f"\n[Transacción {n}] frame #{frame} | nonce={nonce.hex()} | tag OK")
        print(msg.decode())
    except Exception:
        print(f"\n[Transacción {n}] frame #{frame} | FALLÓ la autenticación")

print(f"\n[+] {ok}/{len(txs)} transacciones descifradas y autenticadas correctamente")
