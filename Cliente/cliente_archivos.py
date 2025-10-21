import socket
import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import os

HOST = 'localhost'  # O la IP del servidor si está en otra máquina
PORT = 5000
BUFFER_SIZE = 1024

def subir_archivo():
    threading.Thread(target=enviar_archivo, daemon=True).start()

def enviar_archivo():
    filepath = filedialog.askopenfilename(title="Seleccionar archivo para enviar")
    if not filepath:
        return

    filename = os.path.basename(filepath)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(filename.encode())

            response = s.recv(BUFFER_SIZE)
            if response == b"READY":
                with open(filepath, "rb") as f:
                    while chunk := f.read(BUFFER_SIZE):
                        s.send(chunk)
                s.send(b"EOF")
                mostrar_mensaje(f"✅ Archivo '{filename}' enviado correctamente.")
            else:
                mostrar_mensaje("❌ El servidor no aceptó la transferencia.")
    except Exception as e:
        mostrar_mensaje(f"⚠️ Error: {e}")

def mostrar_mensaje(msg):
    root.after(0, lambda: _mostrar_mensaje(msg))

def _mostrar_mensaje(msg):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, msg + "\n")
    text_area.config(state=tk.DISABLED)
    text_area.yview(tk.END)

# GUI
root = tk.Tk()
root.title("Cliente de Archivos")
root.geometry("400x300")

btn = tk.Button(root, text="📤 Enviar archivo al servidor", command=subir_archivo)
btn.pack(pady=10)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
