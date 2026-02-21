import os
import shutil
from sftp_service import conectar_sftp
from zipar_file import baixar_recursivo, zipar_pasta
import tempfile
from pathlib import Path

BASE_REMOTA = "/sftp-assessoria-prd/Fortes-Assessoria/Cobaas/Enviados/Documentos"


def executar_contrato(contrato: str) -> str:
    if not contrato:
        return "Contrato não informado."

    pasta_remota = f"{BASE_REMOTA}/{contrato}"
    DOWNLOADS_DIR = Path.home() / "Downloads"
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

    pasta_local = Path(tempfile.gettempdir()) / f"temp_{contrato}"
    zip_nome = DOWNLOADS_DIR / f"{contrato}.zip"

    sftp, transport = conectar_sftp()

    try:
        qtd_arquivos = baixar_recursivo(sftp, pasta_remota, pasta_local)

        if qtd_arquivos == 0:
            return f"Erro: O contrato {contrato} não foi encontrado ou não possui arquivos no servidor."

        # 3. Só tenta zipar se houve sucesso no download
        if zipar_pasta(pasta_local, zip_nome):
            return f"Contrato {contrato} baixado com sucesso!\nTotal de arquivos: {qtd_arquivos}\nSalvo em: {zip_nome}"
        else:
            return f"Erro ao gerar o arquivo ZIP para o contrato {contrato}."

    except Exception as e:
        return f"Erro ao processar contrato {contrato}:\n{e}"

    finally:
        sftp.close()
        transport.close()
        if pasta_local.exists():
            shutil.rmtree(pasta_local)


def main():
    contrato = input("Qual o contrato? ").strip()
    resultado = executar_contrato(contrato)
    print(resultado)


if __name__ == "__main__":
    main()