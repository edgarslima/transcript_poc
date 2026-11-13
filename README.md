# Transcrição local de áudio e vídeo

Ferramenta de linha de comando para transcrever arquivos de áudio e vídeo localmente. Gera uma transcrição em texto (`.txt`) e legendas com marcações de tempo (`.srt`).

O projeto usa modelos Whisper por meio de `mlx-whisper` ou `faster-whisper`. A transcrição é executada no computador; a instalação das dependências e o primeiro uso de um modelo baixado exigem conexão com a internet.

## Plataformas e requisitos

Todas as plataformas precisam de **Python 3.11 ou superior**, `pip` e espaço em disco para as dependências, os modelos e os arquivos de saída. A memória e o tempo de processamento variam conforme o modelo e o tamanho da entrada; este projeto não definiu um mínimo de RAM ou disco por meio de testes.

| Plataforma | Requisitos para a configuração descrita abaixo | Motor |
| --- | --- | --- |
| macOS | macOS 14 ou superior, processador Apple Silicon, Python nativo para ARM e ffmpeg. | `mlx-whisper` |
| Linux | Processador x86-64 com SSE 4.1 ou ARM64, Python e Bash. | `faster-whisper` em CPU, com precisão int8 |
| Windows | Sistema e processador x86-64 com SSE 4.1, Python e PowerShell. Pode ser necessário instalar o runtime Microsoft Visual C++. | `faster-whisper` em CPU, com precisão int8 |

Os requisitos de sistema dependem também das versões e dos pacotes disponíveis para cada plataforma. Consulte a documentação do [MLX](https://github.com/ml-explore/mlx/blob/main/docs/src/install.rst), do [faster-whisper](https://github.com/SYSTRAN/faster-whisper) e do [CTranslate2](https://github.com/OpenNMT/CTranslate2/blob/master/docs/installation.md).

## Instalação e uso

Execute os comandos na pasta do projeto e substitua o caminho de entrada pelo arquivo desejado.

### macOS

```bash
brew install ffmpeg
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./transcript.sh ~/Downloads/entrada.m4a
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-windows.txt
./transcript.sh --backend faster-whisper ~/Downloads/entrada.m4a
```

O arquivo `requirements-windows.txt` também fornece as dependências do motor usado no Linux. Em algumas distribuições, é necessário instalar o pacote do sistema que fornece `venv` para o Python.

### Windows

No PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-windows.txt
.\transcript.ps1 "$HOME\Downloads\entrada.m4a"
```

O `faster-whisper` decodifica mídia por meio do PyAV e não exige uma instalação separada do executável ffmpeg.

## Saída e opções

Por padrão, os arquivos são criados em `output/` na pasta do projeto, com o nome da entrada. Por exemplo, `entrada.m4a` gera `output/entrada.txt` e `output/entrada.srt`. O idioma padrão é português. Arquivos de saída com o mesmo nome são sobrescritos.

É possível definir a pasta ou o nome de saída, o idioma e o modelo. Consulte [transcript_doc.md](transcript_doc.md) para o script Bash e [transcript_doc_ps.md](transcript_doc_ps.md) para PowerShell. No Linux, acrescente `--backend faster-whisper` aos exemplos Bash e escolha um modelo compatível com esse motor.

## Testes

```bash
python -m unittest discover -s tests -v
```

Use `python3` caso `python` não esteja disponível. Os testes simulam os motores e não precisam baixar modelos. Para executá-los antes dos commits, configure o hook uma vez por clone:

```bash
git config --local core.hooksPath .githooks
```

O hook verifica os arquivos preparados para o commit e pode ser ignorado localmente. No GitHub, a proteção da `main` exige a aprovação dos testes antes da incorporação de alterações.
