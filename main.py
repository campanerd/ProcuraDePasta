import os
import shutil
import tempfile
from pathlib import Path

from conectsftp_service import conectar_sftp
from zipar_file import zipar_pasta
from down_service import baixar_recursivo

BASE_REMOTA = "/sftp-assessoria-prd/Fortes-Assessoria/Cobaas/Enviados/Documentos"


def encontrar_pasta_por_prefixo(sftp, base_remota, contrato):
    for attr in sftp.listdir_iter(base_remota):
        if attr.filename.startswith(contrato):
            return f"{base_remota}/{attr.filename}"
    return None

def executar_contrato(contrato: str) -> str:
    if not contrato:
        return "Contrato não informado."

    DOWNLOADS_DIR = Path.home() / "Downloads"
    pasta_local = Path(tempfile.gettempdir()) / f"temp_{contrato}"

    sftp = None
    transport = None

    try:
        sftp, transport = conectar_sftp()

        pasta_remota = encontrar_pasta_por_prefixo(sftp, BASE_REMOTA, contrato)
        if not pasta_remota:
            return f"Nenhuma pasta encontrada iniciando com: {contrato}"

        nome_pasta = pasta_remota.split("/")[-1]
        zip_nome = DOWNLOADS_DIR / f"{nome_pasta}.zip"

        qtd_arquivos = baixar_recursivo(sftp, pasta_remota, pasta_local)

        if qtd_arquivos == 0:
            return f"A pasta do contrato {contrato} existe, mas está vazia (sem arquivos)."

        if zipar_pasta(pasta_local, zip_nome):
            return (
                f"Contrato {contrato} baixado com sucesso!\n"
                f"Total de arquivos: {qtd_arquivos}\n"
                f"Salvo em: {zip_nome}"
            )

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