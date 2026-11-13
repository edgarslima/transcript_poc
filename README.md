# POC — Transcrição de Áudio Local

CLI para transcrever áudio e vídeo localmente em um Mac com Apple Silicon, usando mlx-whisper.

## Requisitos e instalação

- Python 3.11 ou superior
- ffmpeg
- Ambiente virtual Python com as dependências do projeto

```bash
brew install ffmpeg
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
./transcript.sh ~/Downloads/entrada.m4a
```

Por padrão, o comando cria `output/entrada.txt` e `output/entrada.srt` na pasta do projeto. Consulte [transcript_doc.md](transcript_doc.md) para todas as opções e exemplos.

## Windows

No Windows, use `transcript.ps1` com faster-whisper. A instalação e os exemplos estão em [transcript_doc_ps.md](transcript_doc_ps.md).

## Testes e proteção da main

Execute a suíte com Python 3.11 ou superior, sem instalar os modelos de transcrição:

```bash
python -m unittest discover -s tests -v
```

No macOS, se necessário, use `python3` no lugar de `python`. Os testes simulam os motores de transcrição e verificam os scripts disponíveis, sem baixar modelos ou arquivos de mídia.

Após inicializar ou clonar o repositório Git, instale o hook local uma vez por clone:

```bash
git config --local core.hooksPath .githooks
```

O hook executa os testes sobre os arquivos preparados com `git add` e bloqueia o commit se eles falharem. Instalar o hook substitui qualquer outro `core.hooksPath` configurado localmente. Hooks locais podem ser desativados ou ignorados, portanto não garantem a proteção da branch no servidor.

O workflow `.github/workflows/tests.yml` executa a suíte em Linux, macOS e Windows. Para proteger a `main` no GitHub, publique o workflow e, em **Settings → Branches**, crie uma regra para `main`: exija pull requests e o status **testes-obrigatorios**; impeça que administradores e outras funções ignorem as regras e restrinja permissões de bypass. O status precisa ter sido executado pelo menos uma vez para aparecer na seleção. Essa configuração exige permissões de administração e disponibilidade de regras de proteção no plano do repositório. Com ela, alterações só entram na `main` do GitHub após a verificação exigida; commits locais ainda podem ser feitos ou seus hooks ignorados.
