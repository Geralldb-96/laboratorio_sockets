import socket
import threading

HOST = 'localhost'
PORT = 6000
clientes = []
clientes_lock = threading.Lock()

def manejar_cliente(conn, addr):
    print(f"Cliente conectado: {addr}")
    while True:
        try:
            mensaje = conn.recv(1024).decode()
            if not mensaje:
                break
            print(f"{addr}: {mensaje}")
            with clientes_lock:
                for c in clientes:
                    if c != conn:
                        try:
                            c.send(f"{addr}: {mensaje}".encode())
                        except:
                            # Ignorar errores de envío (por ejemplo cliente desconectado)
                            pass
        except:
            break
    # Cuando sale del bucle, el cliente se desconectó o hubo error
    with clientes_lock:
        if conn in clientes:
            clientes.remove(conn)
    conn.close()
    print(f"Cliente desconectado: {addr}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor de chat en {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with clientes_lock:
            clientes.append(conn)
        threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()
