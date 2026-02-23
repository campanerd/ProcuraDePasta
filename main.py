import os
import shutil
from conectsftp_service import conectar_sftp
from zipar_file import zipar_pasta
from down_service import baixar_recursivo
import tempfile
from pathlib import Path

BASE_REMOTA = "/sftp-assessoria-prd/Fortes-Assessoria/Cobaas/Enviados/Documentos"

def encontrar_pasta_contrato(sftp, base_remota, termo_busca):
    pastas = sftp.listdir_attr(base_remota)
    for attr in pastas:
        if termo_busca.lower() in attr.filename.lower():
            return f"{base_remota}/{attr.filename}"
    return None

def executar_contrato(contrato: str) -> str:
    if not contrato:
        return "Contrato não informado."

    DOWNLOADS_DIR = Path.home() / "Downloads"
    pasta_local = Path(tempfile.gettempdir()) / f"temp_{contrato}"
    zip_nome = DOWNLOADS_DIR / f"{contrato}.zip"

    sftp = None
    transport = None

    try:
        sftp, transport = conectar_sftp()

        pasta_remota = encontrar_pasta_contrato(sftp, BASE_REMOTA, contrato)
        if not pasta_remota:
            return f"Nenhuma pasta encontrada contendo: {contrato}"

        qtd_arquivos = baixar_recursivo(sftp, pasta_remota, pasta_local)

        if qtd_arquivos == 0:
            return f"A pasta do contrato {contrato} existe, mas está vazia (sem arquivos)."

        if zipar_pasta(pasta_local, zip_nome):
            return f"Contrato {contrato} baixado com sucesso!\nTotal de arquivos: {qtd_arquivos}\nSalvo em: {zip_nome}"

        return "Erro ao gerar o arquivo ZIP."

    except Exception as e:
        return f"Erro inesperado: {e}"

    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()
        if pasta_local.exists():
            shutil.rmtree(pasta_local)

def main():
    contrato = input("Qual o contrato? ").strip()
    resultado = executar_contrato(contrato)
    print(resultado)

if __name__ == "__main__":
    main()