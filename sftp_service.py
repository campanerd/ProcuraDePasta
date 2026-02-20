import paramiko
import os
from pathlib import Path
from zipfile import ZipFile
from dotenv import load_dotenv

load_dotenv()

def down_ocorrencias(contrato: str):
    BASE_DIR = Path(__file__).resolve().parent

    DOWNLOADS_DIR = BASE_DIR / "src" / "files"
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

    SFTP_HOST = os.getenv("SFTP_HOST")
    SFTP_USER = os.getenv("SFTP_USER")
    SFTP_PASS = os.getenv("SFTP_PASS")
    SFTP_PORT = int(os.getenv("SFTP_PORT", 22))

    CAMINHO_BASE = os.getenv("SFTP_CAMINHO")
    pasta_remota = f"{CAMINHO_BASE}/{contrato}"

    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)

        try:
            arquivos = sftp.listdir(pasta_remota)
        except FileNotFoundError:
            print(f"Pasta do contrato {contrato} não encontrada.")
            return

        if not arquivos:
            print(f"Pasta do contrato {contrato} existe, mas está vazia.")
            return

        zip_path = DOWNLOADS_DIR / f"{contrato}.zip"

        with ZipFile(zip_path, "w") as zipf:
            for nome_arquivo in arquivos:
                remoto = f"{pasta_remota}/{nome_arquivo}"
                local = DOWNLOADS_DIR / nome_arquivo

                sftp.get(remoto, local)
                zipf.write(local, arcname=nome_arquivo)
                local.unlink()

        print(f"Contrato {contrato} baixado com sucesso em {zip_path}")

        sftp.close()
        transport.close()

    except Exception as e:
        print("Erro ao processar o download via SFTP")
        print(e)


if __name__ == "__main__":
    contrato = input("Qual o contrato? ").strip()

    if not contrato:
        print("Contrato não informado.")
    else:
        down_ocorrencias(contrato)
