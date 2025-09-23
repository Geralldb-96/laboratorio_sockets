import socket
import threading

HOST = 'localhost'
PORT = 6000
CHUNK_SIZE = 4 * 1024 * 1024  # 4 MB
clientes = {}
usuarios_validos = {
    "ana": "123",
    "juan": "abc",
    "maria": "pass"
}

def manejar_cliente(conn, addr):
    try:
        # --- Login ---
        credenciales = conn.recv(1024).decode()
        if ":" not in credenciales:
            conn.send(b"ERROR")
            conn.close()
            return
        usuario, contrasena = credenciales.split(":", 1)

        if usuarios_validos.get(usuario) != contrasena:
            conn.send(b"ERROR")
            conn.close()
            return

        conn.send(b"OK")
        clientes[conn] = usuario
        print(f"Cliente {usuario} conectado desde {addr}")

        # --- Bucle de mensajes ---
        while True:
            header = conn.recv(1024)
            if not header:
                break

            if header.startswith(b"FILE:"):  # --- caso archivo ---
                try:
                    parts = header.decode().split(":", 2)
                    _, nombre, tamano = parts
                    tamano = int(tamano)

                    print(f"[{usuario}] envió un archivo: {nombre} ({tamano/1024/1024:.2f} MB)")

                    # reenviar cabecera a los demás
                    for c in list(clientes.keys()):
                        if c != conn:
                            c.send(header)

                    # leer y reenviar en fragmentos
                    recibido = 0
                    while recibido < tamano:
                        chunk = conn.recv(min(CHUNK_SIZE, tamano - recibido))
                        if not chunk:
                            break
                        recibido += len(chunk)
                        # reenviar a todos
                        for c in list(clientes.keys()):
                            if c != conn:
                                c.sendall(chunk)

                except Exception as e:
                    print("Error al manejar archivo:", e)
                    break

            else:  # --- caso texto ---
                mensaje = header.decode()
                msg_final = f"[{usuario}] {mensaje}"
                print(msg_final)
                for c in list(clientes.keys()):
                    if c != conn:
                        try:
                            c.send(msg_final.encode())
                        except:
                            c.close()
                            del clientes[c]
    except:
        pass
    finally:
        if conn in clientes:
            print(f"{clientes[conn]} se desconectó")
            del clientes[conn]
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor de chat con login+archivos en {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()
