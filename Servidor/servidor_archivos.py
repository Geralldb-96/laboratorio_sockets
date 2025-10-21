import socket
import os

HOST = '0.0.0.0'  # Escucha en todas las interfaces (útil para Docker)
PORT = 5000
BUFFER_SIZE = 1024

# Crear socket TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"📡 Servidor escuchando en {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        print(f"🟢 Conexión establecida con {addr}")

        # Recibir nombre del archivo
        filename = conn.recv(BUFFER_SIZE).decode()
        if not filename:
            conn.close()
            continue

        print(f"📂 Recibiendo archivo: {filename}")
        conn.send(b"READY")

        # Guardar archivo con prefijo 'recibido_'
        with open("recibido_" + filename, "wb") as f:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if data == b"EOF" or not data:
                    break
                f.write(data)

        print(f"✅ Archivo '{filename}' recibido correctamente.")
        conn.close()
