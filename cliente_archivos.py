# cliente_archivos.py
import socket

HOST = '127.0.0.1'
PORT = 5000
BUFFER_SIZE = 4096

filename = input("Nombre del archivo a descargar (ej: hola.txt): ").strip()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(filename.encode())

    # esperamos respuesta corta: b"OK" o b"NO"
    response = s.recv(2)
    if response == b"OK":
        out_name = "recibido_" + filename
        with open(out_name, "wb") as f:
            while True:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
        print("Archivo recibido con éxito:", out_name)
    else:
        print("Servidor respondió: archivo no encontrado.")
