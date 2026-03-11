# Busca e Download de Contratos via SFTP

Este projeto automatiza a busca, download e compactação de documentos armazenados em um servidor SFTP.
O usuário informa apenas o **número do contrato**, e o sistema localiza automaticamente a pasta correspondente no servidor, realiza o download de todos os arquivos e gera um **arquivo .zip** contendo os documentos.

O sistema foi desenvolvido para lidar com diretórios muito grandes no servidor, evitando carregamentos completos de pastas e melhorando o desempenho da busca.

---

## Funcionalidades

* Busca de pastas por **prefixo do número do contrato**
* Conexão automática com servidor **SFTP**
* Download recursivo de todos os arquivos da pasta
* Compactação automática dos arquivos em **.zip**
* Armazenamento do arquivo final na pasta **Downloads do usuário**
* Limpeza automática de arquivos temporários
* Tratamento de erros durante conexão, busca ou download

---

## Tecnologias utilizadas

* **Python**
* **Paramiko** (conexão SFTP)
* **Pathlib**
* **Tempfile**
* **Zipfile**

---

## Estrutura do projeto

```
projeto/
│
├── app.py
├── main.py
│
├── conectsftp_service.py
├── down_service.py
├── zipar_file.py
│
└── README.md
```

### Arquivos principais

**app.py**

Responsável pela interface de execução do sistema.

**main.py**

Contém a lógica principal:

* conexão com o SFTP
* busca da pasta do contrato
* download dos arquivos
* geração do arquivo zip

**conectsftp_service.py**

Gerencia a conexão com o servidor SFTP.

**down_service.py**

Realiza o download recursivo de todos os arquivos da pasta encontrada.

**zipar_file.py**

Compacta os arquivos baixados em um único arquivo `.zip`.

---

## Como funciona

1. O usuário informa o **número do contrato**.
2. O sistema se conecta ao servidor **SFTP**.
3. O programa percorre as pastas do diretório remoto até encontrar uma que **comece com o número do contrato**.
4. Após encontrar a pasta:

   * todos os arquivos são baixados
   * os arquivos são compactados em um `.zip`
5. O arquivo final é salvo em:

```
C:\Users\<usuario>\Downloads
```

---

## Exemplo de execução

```
Qual o contrato? 61482
Contrato 61482 baixado com sucesso!
Total de arquivos: 27
Salvo em: C:\Users\usuario\Downloads\61482 - ANA CLEIA DA SILVA REIS.zip
```

---

## Requisitos

* Python **3.10 ou superior**
* Biblioteca:

```
paramiko
```

Instalação:

```
pip install paramiko
```

---

## Observações importantes

O servidor SFTP pode conter **um grande volume de pastas**, o que pode impactar o tempo de busca.
Para evitar travamentos, o sistema utiliza **listagem iterativa de diretórios**, permitindo interromper a busca assim que a pasta correta é encontrada.

---

