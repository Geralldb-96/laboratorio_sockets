import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import os

HOST = 'localhost'
PORT = 6000
CHUNK_SIZE = 4 * 1024 * 1024  # 4 MB por bloque

class ChatClienteGUI:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        self.usuario = None

        # --- ventana login ---
        self.login_win = tk.Tk()
        self.login_win.title("Login Chat")

        tk.Label(self.login_win, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.login_win, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)

        self.entry_usuario = tk.Entry(self.login_win)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)

        self.entry_contra = tk.Entry(self.login_win, show="*")
        self.entry_contra.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_win, text="Ingresar", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

        self.login_win.mainloop()

    def login(self):
        usuario = self.entry_usuario.get().strip()
        contra = self.entry_contra.get().strip()
        self.sock.send(f"{usuario}:{contra}".encode())
        resp = self.sock.recv(1024).decode()
        if resp == "OK":
            self.usuario = usuario
            self.login_win.destroy()
            self.iniciar_chat()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def iniciar_chat(self):
        self.chat_win = tk.Tk()
        self.chat_win.title(f"Chat - Usuario: {self.usuario}")

        self.text_area = scrolledtext.ScrolledText(self.chat_win, wrap=tk.WORD, state='disabled', width=60, height=20)
        self.text_area.pack(padx=10, pady=10)

        frame = tk.Frame(self.chat_win)
        frame.pack(pady=5)

        self.entry = tk.Entry(frame, width=40)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", self.enviar)

        self.send_button = tk.Button(frame, text="Enviar", command=self.enviar)
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.file_button = tk.Button(frame, text="Adjuntar archivo", command=self.enviar_archivo)
        self.file_button.pack(side=tk.LEFT, padx=5)

        os.makedirs("descargas", exist_ok=True)

        threading.Thread(target=self.recibir, daemon=True).start()
        self.chat_win.mainloop()

    def enviar(self, event=None):
        msg = self.entry.get()
        if msg:
            self.sock.send(msg.encode())
            self.entry.delete(0, tk.END)

    def enviar_archivo(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        nombre = os.path.basename(filepath)
        tamano = os.path.getsize(filepath)
        header = f"FILE:{nombre}:{tamano}".encode()
        self.sock.send(header)

        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                self.sock.sendall(chunk)

        self.mostrar_texto(f"[Tú] enviaste un archivo: {nombre} ({tamano/1024/1024:.2f} MB)")

    def recibir(self):
        while True:
            try:
                header = self.sock.recv(1024)
                if not header:
                    break

                if header.startswith(b"FILE:"):
                    parts = header.decode().split(":", 2)
                    _, nombre, tamano = parts
                    tamano = int(tamano)

                    path = os.path.join("descargas", nombre)
                    with open(path, "wb") as f:
                        recibido = 0
                        while recibido < tamano:
                            chunk = self.sock.recv(min(CHUNK_SIZE, tamano - recibido))
                            if not chunk:
                                break
                            f.write(chunk)
                            recibido += len(chunk)

                    self.mostrar_texto(f"Archivo recibido: {nombre} ({tamano/1024/1024:.2f} MB, guardado en descargas/)")
                else:
                    self.mostrar_texto(header.decode())
            except:
                break

    def mostrar_texto(self, msg):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, msg + "\n")
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

if __name__ == "__main__":
    ChatClienteGUI()
