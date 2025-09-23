# servidor_archivos.py
import socket
import os

HOST = '127.0.0.1'   # localhost
PORT = 5000
BUFFER_SIZE = 4096

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor esperando en {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Conexión establecida con {addr}")
            filename = conn.recv(1024).decode().strip()
            if not filename:
                print("No se recibió nombre de archivo.")
                continue

            print("Archivo solicitado:", filename)
            if os.path.exists(filename) and os.path.isfile(filename):
                conn.sendall(b"OK")  # cabecera corta (2 bytes)
                with open(filename, "rb") as f:
                    while True:
                        chunk = f.read(BUFFER_SIZE)
                        if not chunk:
                            break
                        conn.sendall(chunk)
                print("Archivo enviado con éxito:", filename)
            else:
                conn.sendall(b"NO")
                print("Archivo no encontrado:", filename)
