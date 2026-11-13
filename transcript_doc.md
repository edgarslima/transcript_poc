# Uso do transcript.sh

O script transcreve um arquivo de áudio ou vídeo e produz dois arquivos: texto (`.txt`) e legendas com marcações de tempo (`.srt`). O processamento usa o mlx-whisper; é necessário um Mac com Apple Silicon, Python 3.11 ou superior, ffmpeg e as dependências instaladas como descrito no [README](README.md). A primeira execução de um modelo pode precisar baixá-lo.

## Sintaxe

```text
./transcript.sh [opções] arquivo_de_entrada
```

O arquivo de entrada é obrigatório. Caminhos relativos são interpretados a partir do diretório em que o comando é executado. Coloque caminhos com espaços entre aspas.

| Parâmetro | Função | Padrão |
| --- | --- | --- |
| `arquivo_de_entrada` | Caminho do áudio ou vídeo a transcrever. | Obrigatório. |
| `-o`, `--output CAMINHO` | Caminho base para as saídas, sem `.txt` ou `.srt`. As duas extensões são acrescentadas. | Nome do arquivo de entrada sem a última extensão, em `output/` na pasta do projeto. |
| `-d`, `--output-dir PASTA` | Pasta das saídas, mantendo o nome base da entrada. Não pode ser combinado com `--output`. | `output/` na pasta do projeto. |
| `-m`, `--model MODELO` | Nome do repositório do modelo ou caminho de um modelo local compatível com mlx-whisper. | `mlx-community/whisper-large-v3-mlx` |
| `-l`, `--language CÓDIGO` | Código do idioma passado ao modelo, por exemplo `pt` ou `en`. | `pt` |
| `--python CAMINHO` | Interpretador Python com mlx-whisper instalado. | Ambiente virtual ativo, `.venv`, `venv` ou `python3` no PATH, nessa ordem. |
| `-h`, `--help` | Mostra a ajuda. | — |

A variável de ambiente `PYTHON` também permite escolher o interpretador; `--python` tem prioridade. As pastas de saída ausentes são criadas. Arquivos `.txt` e `.srt` existentes com os mesmos nomes são sobrescritos.

## Exemplos

Transcrever um áudio e gerar `output/entrada.txt` e `output/entrada.srt`:

```bash
./transcript.sh ~/Downloads/entrada.mp3
```

Transcrever um vídeo cujo caminho contém espaços; não é criado um arquivo intermediário de áudio:

```bash
./transcript.sh "$HOME/Downloads/arquivo de exemplo.mov"
```

Use `$HOME` em caminhos entre aspas: o shell não expande `~` dentro de aspas.

Escolher a pasta e manter o nome da entrada (`resultados/entrada.txt` e `resultados/entrada.srt`):

```bash
./transcript.sh --output-dir resultados ~/Downloads/entrada.mp4
```

Escolher o caminho e o nome base dos dois arquivos (`resultados/saida.txt` e `.srt`):

```bash
./transcript.sh --output resultados/saida ~/Downloads/entrada.wav
```

Escolher idioma e modelo:

```bash
./transcript.sh --language en --model mlx-community/whisper-small-mlx ~/Downloads/entrada.m4a
```

Usar um modelo local e um Python específico:

```bash
./transcript.sh --python "$HOME/ambientes/transcricao/bin/python" --model "$HOME/modelos/whisper" ~/Downloads/audio.wav
```

Usar a variável de ambiente para selecionar o Python:

```bash
PYTHON="$HOME/ambientes/transcricao/bin/python" ./transcript.sh ~/Downloads/audio.wav
```

Ver a ajuda ou tratar um nome de entrada iniciado por hífen:

```bash
./transcript.sh --help
./transcript.sh -- -entrada.mp3
```

O script também aceita as formas curtas `-o`, `-d`, `-m` e `-l`. O programa `transcribe.py` pode ser executado diretamente com as mesmas opções de transcrição; `--python` é exclusivo do script de shell.
