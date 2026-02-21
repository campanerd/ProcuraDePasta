import os
import stat
import zipfile

def baixar_recursivo(sftp, remoto, local):
    arquivos_contagem = 0
    itens = sftp.listdir_attr(remoto)
    
    if itens:
        os.makedirs(local, exist_ok=True)

    for item in itens:
        remoto_item = f"{remoto}/{item.filename}"
        local_item = os.path.join(local, item.filename)

        if stat.S_ISDIR(item.st_mode):
            arquivos_contagem += baixar_recursivo(sftp, remoto_item, local_item)
        else:
            sftp.get(remoto_item, local_item)
            arquivos_contagem += 1
            
    return arquivos_contagem

def zipar_pasta(pasta, zip_nome):
    # Só tenta zipar se a pasta local realmente existir e tiver algo
    if not os.path.exists(pasta) or not os.listdir(pasta):
        return False
        
    with zipfile.ZipFile(zip_nome, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(pasta):
            for file in files:
                caminho_completo = os.path.join(root, file)
                arcname = os.path.relpath(caminho_completo, pasta)
                zipf.write(caminho_completo, arcname)
    return True