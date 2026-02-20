import tkinter as tk
from tkinter import messagebox
import threading
from main import executar_contrato

def iniciar():
    contrato = entry.get().strip()
    if not contrato:
        messagebox.showwarning("Aviso", "Informe o contrato")
        return

    status.config(text="Processando...")
    threading.Thread(
        target=executar,
        args=(contrato,),
        daemon=True
    ).start()

def executar(contrato):
    try:
        executar_contrato(contrato)
        status.config(text="Finalizado")
    except Exception as e:
        status.config(text="Erro")
        messagebox.showerror("Erro", str(e))

root = tk.Tk()
root.title("Download SFTP")
root.geometry("300x150")

tk.Label(root, text="Contrato").pack(pady=5)
entry = tk.Entry(root)
entry.pack()

tk.Button(root, text="Baixar", command=iniciar).pack(pady=10)
status = tk.Label(root, text="")
status.pack()

root.mainloop()