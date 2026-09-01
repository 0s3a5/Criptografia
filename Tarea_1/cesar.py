import sys

def cifrar_cesar(texto, corrimiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            ascii_base = ord('a') if char.islower() else ord('A')
            resultado += chr((ord(char) - ascii_base + corrimiento) % 26 + ascii_base)
        else:
            resultado += char
    return resultado

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 cesar.py \"texto\" <corrimiento>")
        sys.exit(1)
   
    texto = sys.argv[1]
    corrimiento = int(sys.argv[2])
    print(cifrar_cesar(texto, corrimiento))
