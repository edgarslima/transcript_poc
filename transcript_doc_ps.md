# Uso do transcript.ps1 no Windows

O script transcreve um arquivo de áudio ou vídeo e gera texto (`.txt`) e legendas (`.srt`). No Windows, usa [faster-whisper](https://github.com/SYSTRAN/faster-whisper), pois o motor MLX usado no Mac não oferece suporte ao Windows. A transcrição usa CPU com precisão int8; GPU não é configurada por este script. Os modelos para MLX e faster-whisper têm formatos diferentes.

## Instalação

No PowerShell, dentro da pasta do projeto, com Python 3.11 ou superior instalado:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-windows.txt
```

Não é necessário ativar o ambiente virtual: o script encontra `.venv` automaticamente. O faster-whisper usa PyAV para decodificar mídia e não exige instalar o executável ffmpeg separadamente. O primeiro uso de um modelo pelo nome pode baixá-lo e requer conexão à internet.

Se a política do PowerShell impedir a execução de scripts locais, consulte as regras da sua organização. Para uma sessão em que seja permitido, pode-se executar `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`; isso só afeta a sessão atual. Para scripts baixados da internet, pode ser necessário desbloquear o arquivo com `Unblock-File .\transcript.ps1`.

## Sintaxe

```text
.\transcript.ps1 [-Entrada] ARQUIVO [-Output CAMINHO | -OutputDir PASTA] [-Model MODELO] [-Language CÓDIGO] [-Python CAMINHO]
```

Caminhos relativos são interpretados a partir do diretório atual. Coloque caminhos com espaços entre aspas.

| Parâmetro | Função | Padrão |
| --- | --- | --- |
| `-Entrada` | Caminho do áudio ou vídeo; também pode ser informado sem o nome do parâmetro. | Obrigatório. |
| `-Output`, `-o` | Caminho base dos arquivos de saída, sem extensão; acrescenta `.txt` e `.srt`. | Nome da entrada sem a última extensão, em `output\` na pasta do projeto. |
| `-OutputDir`, `-d` | Pasta de saída, mantendo o nome base da entrada. Não combine com `-Output`. | `output\` na pasta do projeto. |
| `-Model`, `-m` | Nome ou caminho local de modelo compatível com faster-whisper/CTranslate2. | `large-v3` |
| `-Language`, `-l` | Código do idioma, por exemplo `pt` ou `en`. | `pt` |
| `-Python` | Interpretador Python com faster-whisper instalado. | Ambiente virtual ativo, `.venv`, `venv` ou `python` no PATH, nessa ordem. |
| `-Help`, `-h` | Mostra a ajuda. | — |

A variável de ambiente `$env:PYTHON` também seleciona o interpretador; `-Python` tem prioridade. As pastas de saída ausentes são criadas. Arquivos `.txt` e `.srt` existentes com os mesmos nomes são sobrescritos.

## Exemplos

Transcrever um áudio e gerar `output\entrada.txt` e `output\entrada.srt`:

```powershell
.\transcript.ps1 "$HOME\Downloads\entrada.mp3"
```

Transcrever um vídeo com espaços no nome, informando o parâmetro de entrada:

```powershell
.\transcript.ps1 -Entrada "$HOME\Downloads\arquivo de exemplo.mov"
```

Escolher a pasta, mantendo o nome da entrada:

```powershell
.\transcript.ps1 "$HOME\Downloads\entrada.mp4" -OutputDir .\resultados
```

Escolher o caminho e o nome base de ambos os arquivos:

```powershell
.\transcript.ps1 "$HOME\Downloads\entrada.wav" -Output .\resultados\saida
```

Escolher idioma e modelo; um modelo menor pode ser mais rápido em CPU:

```powershell
.\transcript.ps1 "$HOME\Downloads\entrada.m4a" -Language en -Model small
```

Usar um modelo local e um interpretador específico:

```powershell
.\transcript.ps1 "$HOME\Downloads\audio.wav" -Model "$HOME\modelos\whisper" -Python "$HOME\ambientes\transcricao\Scripts\python.exe"
```

Selecionar o interpretador por variável de ambiente:

```powershell
$env:PYTHON = "$HOME\ambientes\transcricao\Scripts\python.exe"
.\transcript.ps1 "$HOME\Downloads\audio.wav"
Remove-Item Env:PYTHON
```

Usar abreviações ou consultar a ajuda:

```powershell
.\transcript.ps1 "$HOME\Downloads\audio.wav" -d .\resultados -l pt -m small
.\transcript.ps1 -Help
```
