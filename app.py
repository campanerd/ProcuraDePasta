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
    botao.config(state="disabled")

    threading.Thread(
        target=executar_em_thread,
        args=(contrato,),
        daemon=True
    ).start()

def executar_em_thread(contrato):
    resultado = executar_contrato(contrato)

    # atualização SEGURA da interface
    root.after(0, lambda: finalizar(resultado))

def finalizar(mensagem):
    status.config(text=mensagem)
    botao.config(state="normal")

root = tk.Tk()
root.title("Download SFTP")
root.geometry("450x220")

tk.Label(root, text="Contrato").pack(pady=5)

entry = tk.Entry(root, width=30)
entry.pack()

botao = tk.Button(root, text="Baixar", command=iniciar)
botao.pack(pady=10)

status = tk.Label(
    root,
    text="",
    wraplength=420,
    justify="left"
)
status.pack(pady=10)

root.mainloop()