import tkinter as tk
from tkinter import messagebox
import threading
from main import executar_contrato, executar_contrato_fast

modo_execucao = None 
entry = None
botao = None


nomes_modo = {
    "normal": "Digitos finais do contrato",
    "fast": "Nome exato da pasta do contrato"
}

def selecionar_opcao(modo):
    global modo_execucao, entry, botao
    modo_execucao = modo

    limpar_frame_inferior()

    tk.Label(frame_inferior, text="Contrato").pack(pady=5)

    entry = tk.Entry(frame_inferior, width=30)
    entry.pack()

    botao = tk.Button(frame_inferior, text="Baixar", command=iniciar)
    botao.pack(pady=10)

    status.config(text=f"Modo selecionado: {nomes_modo[modo]}")

def limpar_frame_inferior():
    for widget in frame_inferior.winfo_children():
        widget.destroy()

def iniciar():
    contrato = entry.get().strip()

    if not contrato:
        messagebox.showwarning("Aviso", "Informe o contrato")
        return

    if not modo_execucao:
        messagebox.showwarning("Aviso", "Selecione uma opção")
        return

    status.config(text="Processando...")
    botao.config(state="disabled")

    if modo_execucao == "normal":
        thread = threading.Thread(
            target=executar_em_thread,
            args=(contrato,),
            daemon=True
        )
    else:
        thread = threading.Thread(
            target=executar_em_thread_fast,
            args=(contrato,),
            daemon=True
        )

    thread.start()


def executar_em_thread(contrato):
    resultado = executar_contrato(contrato)
    root.after(0, lambda: finalizar(resultado))


def executar_em_thread_fast(contrato):
    resultado = executar_contrato_fast(contrato)
    root.after(0, lambda: finalizar(resultado))


def finalizar(mensagem):
    status.config(text=mensagem)
    botao.config(state="normal")


#janela
root = tk.Tk()
root.title("Download SFTP")
root.geometry("450x280")

#frame superior

frame_button = tk.Frame(root)
frame_button.pack(pady=10)

botao1 = tk.Button(frame_button, text="ESPECÍFICO", width=15, command=lambda: selecionar_opcao("normal"))
botao1.pack(side="left", padx=5)

botao2 = tk.Button(frame_button, text="RÁPIDO", width=15, command=lambda: selecionar_opcao("fast"))
botao2.pack(side="left", padx=5)

#frame inferior

frame_inferior = tk.Frame(root)
frame_inferior.pack(expand=True)

tk.Label(
    frame_inferior,
    text="Selecione uma opção acima",
    fg="gray"
).pack(pady=20)

status = tk.Label(
    root,
    text="",
    wraplength=420,
    justify="left"
)
status.pack(pady=5)

tk.Label(
    root,
    text="Desenvolvido por Davi Campaner"
).pack(side="bottom", pady=5)

root.mainloop()