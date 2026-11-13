#!/usr/bin/env bash
# Executa a transcrição de um arquivo de áudio ou vídeo.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python="${PYTHON:-}"
args=()
while (($#)); do
  case "$1" in
    --) args+=("$@"); break ;;
    --python)
      if (($# < 2)) || [[ -z "$2" || "$2" == --* ]]; then
        echo "ERRO: --python exige o caminho do interpretador." >&2
        exit 1
      fi
      python="$2"
      shift 2
      ;;
    *) args+=("$1"); shift ;;
  esac
done

if [[ -z "$python" ]]; then
  if [[ -n "${VIRTUAL_ENV:-}" && -x "$VIRTUAL_ENV/bin/python" ]]; then
    python="$VIRTUAL_ENV/bin/python"
  elif [[ -x "$ROOT/.venv/bin/python" ]]; then
    python="$ROOT/.venv/bin/python"
  elif [[ -x "$ROOT/venv/bin/python" ]]; then
    python="$ROOT/venv/bin/python"
  else
    python=python3
  fi
fi

exec "$python" "$ROOT/transcribe.py" "${args[@]}"
