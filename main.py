import os
import shutil
from sftp_service import conectar_sftp
from zipar_file import baixar_recursivo, zipar_pasta
from pathlib import Path

BASE_REMOTA = "/sftp-assessoria-prd/Fortes-Assessoria/Cobaas/Enviados/Documentos"

def main():
    contrato = input("Qual o contrato? ").strip()

    if not contrato:
        print("Contrato não informado.")
        return

    pasta_remota = f"{BASE_REMOTA}/{contrato}"
    
    BASE_DIR = Path(__file__).resolve().parent
    DOWNLOADS_DIR = BASE_DIR / "src" / "files"
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

    pasta_local = BASE_DIR / f"temp_{contrato}"
    zip_nome = DOWNLOADS_DIR / f"{contrato}.zip"

    sftp, transport = conectar_sftp()

    try:
        conteudo = sftp.listdir(pasta_remota)

        if not conteudo:
            print(f"Pasta do contrato {contrato} está vazia.")
            return

        print("Conteúdo encontrado. Baixando...")

        baixar_recursivo(sftp, pasta_remota, pasta_local)
        zipar_pasta(pasta_local, zip_nome)

        print(f"Contrato {contrato} baixado com sucesso em {zip_nome}")

    except Exception as e:
        print(f"Erro ao processar contrato {contrato}")
        print(e)

    finally:
        sftp.close()
        transport.close()

        if os.path.exists(pasta_local):
            shutil.rmtree(pasta_local)


if __name__ == "__main__":
    main()
