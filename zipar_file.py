import os
import stat
import zipfile

def baixar_recursivo(sftp, remoto, local):
    os.makedirs(local, exist_ok=True)

    for item in sftp.listdir_attr(remoto):
        remoto_item = f"{remoto}/{item.filename}"
        local_item = os.path.join(local, item.filename)

        if stat.S_ISDIR(item.st_mode):
            baixar_recursivo(sftp, remoto_item, local_item)
        else:
            sftp.get(remoto_item, local_item)


def zipar_pasta(pasta, zip_nome):
    with zipfile.ZipFile(zip_nome, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(pasta):
            for file in files:
                caminho_completo = os.path.join(root, file)
                arcname = os.path.relpath(caminho_completo, pasta)
                zipf.write(caminho_completo, arcname)
