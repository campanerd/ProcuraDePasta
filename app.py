import customtkinter as ctk
from tkinter import messagebox
import threading
from main import executar_contrato, executar_contrato_fast

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

modo_execucao = None 

nomes_modo = {
    "normal": "Digitos finais do contrato",
    "fast": "Nome exato da pasta do contrato"
}

def selecionar_opcao(modo):
    global modo_execucao
    modo_execucao = modo

    limpar_frame_inferior()

    ctk.CTkLabel(frame_inferior, text="Contrato").pack(pady=5)

    entry_input = ctk.CTkEntry(frame_inferior, width=200, height=35, placeholder_text="Digite o contrato...")
    entry_input.pack()

    botao_download = ctk.CTkButton(
        frame_inferior,
        text="Baixar",
        height=35,
        corner_radius=8,
        command=lambda: iniciar(entry_input, botao_download)
    )
    botao_download.pack(pady=10)

    status.configure(text=f"Modo selecionado: {nomes_modo[modo]}")

def limpar_frame_inferior():
    for widget in frame_inferior.winfo_children():
        widget.destroy()

def iniciar(entry, botao):
    contrato = entry.get().strip()

    if not contrato:
        messagebox.showwarning("Aviso", "Informe o contrato")
        return

    if not modo_execucao:
        messagebox.showwarning("Aviso", "Selecione uma opção")
        return

    status.configure(text="Processando...")
    botao.configure(state="disabled")

    if modo_execucao == "normal":
        target_func = executar_contrato
    else:
        target_func = executar_contrato_fast

    thread = threading.Thread(
        target=executar_em_thread,
        args=(target_func, contrato, botao),
        daemon=True
    )

    thread.start()


def executar_em_thread(func, contrato, botao):
    try:
        resultado = func(contrato)
    except Exception as e:
        resultado = f"Erro: {str(e)}"

    root.after(0, lambda: finalizar(resultado, botao))


def finalizar(mensagem, botao):
    status.configure(text=mensagem)
    botao.configure(state="normal")


#janela
root = ctk.CTk()
root.title("Download SFTP")
root.geometry("450x300")

#frame superior

frame_button = ctk.CTkFrame(root)
frame_button.pack(pady=(10, 5))

botao1 = ctk.CTkButton(frame_button, text="ESPECÍFICO", width=140, height=35, corner_radius=8, command=lambda: selecionar_opcao("normal"))
botao1.pack(side="left", padx=5)

botao2 = ctk.CTkButton(frame_button, text="RÁPIDO", width=140, height=35, corner_radius=8, command=lambda: selecionar_opcao("fast"))
botao2.pack(side="left", padx=5)

#titulo
ctk.CTkLabel(
    root,
    text="Download de Contratos",
    font=("Arial", 20, "bold")
).pack(pady=(10, 5))

#frame inferior

frame_inferior = ctk.CTkFrame(root, corner_radius=10)
frame_inferior.pack(expand=True, fill="both")

ctk.CTkLabel(
    frame_inferior,
    text="Selecione uma opção acima",
    text_color="gray"
).pack(pady=20)

status = ctk.CTkLabel(
    root,
    text="",
    wraplength=420,
    text_color="gray",
    justify="left",
    font=("Arial", 12)
)
status.pack(pady=5)

ctk.CTkLabel(
    root,
    text="Desenvolvido por Davi Campaner"
).pack(side="bottom", pady=5)

root.mainloop()