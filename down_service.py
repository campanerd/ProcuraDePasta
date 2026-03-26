import os
import stat
import re

def limpar_nome(nome):
    #removendo caracteres inválidos do Windows
    nome = re.sub(r'[<>:"/\\|?*]', '', nome)
    nome = nome.replace('R$', '').replace(',', '')
    return nome[:120]

def baixar_recursivo(sftp, remoto, local, root_call=True):
    arquivos_contagem = 0

    if root_call:
        local = "\\\\?\\" + os.path.abspath(local)

    itens = sftp.listdir_attr(remoto)

    if itens:
        os.makedirs(local, exist_ok=True)

    for item in itens:
        remoto_item = f"{remoto}/{item.filename}"

        nome_limpo = limpar_nome(item.filename)
        local_item = os.path.join(local, nome_limpo)

        if stat.S_ISDIR(item.st_mode):
            arquivos_contagem += baixar_recursivo(
                sftp,
                remoto_item,
                local_item,
                root_call=False  # 🔥 evita duplicar \\?\
            )
        else:
            try:
                sftp.get(remoto_item, local_item)
                arquivos_contagem += 1
            except Exception as e:
                print(f"Erro ao baixar: {remoto_item}")
                print(f"Motivo: {e}")

    return arquivos_contagem