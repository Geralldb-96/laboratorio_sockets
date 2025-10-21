import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = 'localhost'
PORT = 6000

def recibir(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            mostrar_mensaje(data)
        except:
            break

def enviar():
    msg = entry.get()
    if msg:
        try:
            s.send(msg.encode())
            entry.delete(0, tk.END)
        except:
            mostrar_mensaje("❌ Error al enviar mensaje.")

def mostrar_mensaje(msg):
    # Usar root.after para actualizar la GUI desde el hilo principal
    root.after(0, _mostrar_mensaje, msg)

def _mostrar_mensaje(msg):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, msg + "\n")
    text_area.config(state=tk.DISABLED)
    text_area.yview(tk.END)

root = tk.Tk()
root.title("Cliente de Chat")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

frame = tk.Frame(root)
frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(frame)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

btn = tk.Button(frame, text="Enviar", command=enviar)
btn.pack(side=tk.RIGHT, padx=(5,0))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
threading.Thread(target=recibir, args=(s,), daemon=True).start()

root.mainloop()
