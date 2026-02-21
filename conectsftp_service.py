import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

def conectar_sftp():
    host = os.getenv("SFTP_HOST")
    user = os.getenv("SFTP_USER")
    password = os.getenv("SFTP_PASS")
    port = int(os.getenv("SFTP_PORT", 22))

    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    return sftp, transport
