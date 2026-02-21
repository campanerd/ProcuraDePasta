import os
import stat

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