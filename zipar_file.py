import os
import zipfile

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