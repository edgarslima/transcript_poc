#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

MODEL = "mlx-community/whisper-large-v3-mlx"
WINDOWS_MODEL = "large-v3"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def transcribe(audio_path: str, output_base: Path | None = None,
               model: str = MODEL, language: str = "pt", backend: str = "mlx"):
    source_path = Path(audio_path).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {source_path}")

    if backend == "faster-whisper":
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise RuntimeError(
                "faster-whisper não está instalado. Execute: pip install -r requirements-windows.txt"
            ) from exc
        segments, _ = WhisperModel(model, device="cpu", compute_type="int8").transcribe(
            str(source_path), language=language
        )
        segments = list(segments)
        result = {"text": "".join(s.text for s in segments).strip(),
                  "segments": [{"start": s.start, "end": s.end, "text": s.text}
                               for s in segments]}
    else:
        try:
            import mlx_whisper
        except ImportError as exc:
            raise RuntimeError(
                "mlx-whisper não está instalado. Execute: pip install -r requirements.txt"
            ) from exc
        result = mlx_whisper.transcribe(
            str(source_path), path_or_hf_repo=model, language=language
        )

    out_base = (output_base or DEFAULT_OUTPUT_DIR / source_path.stem).expanduser()
    out_base.parent.mkdir(parents=True, exist_ok=True)
    txt_path = Path(f"{out_base}.txt")
    srt_path = Path(f"{out_base}.srt")
    txt_path.write_text(result["text"], encoding="utf-8")

    with srt_path.open("w", encoding="utf-8") as handle:
        for idx, segment in enumerate(result.get("segments", []), start=1):
            handle.write(f"{idx}\n")
            handle.write(f"{_ts(segment['start'])} --> {_ts(segment['end'])}\n")
            handle.write(f"{segment['text'].strip()}\n\n")

    print(f"OK: {txt_path} / {srt_path}")


def _ts(seconds: float) -> str:
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    milliseconds = int((secs % 1) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(secs):02},{milliseconds:03}"


def main():
    parser = argparse.ArgumentParser(
        description="Transcreve áudio ou vídeo em TXT e SRT.",
        epilog="No transcript.sh, use --python CAMINHO para escolher o interpretador.",
    )
    parser.add_argument("entrada", help="arquivo de áudio ou vídeo")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("-o", "--output", help="caminho base de saída, sem extensão")
    destination.add_argument("-d", "--output-dir", help="pasta de saída; usa o nome da entrada")
    parser.add_argument("-m", "--model", help="modelo ou caminho local compatível com o motor")
    parser.add_argument("-l", "--language", default="pt", help="código do idioma (padrão: pt)")
    parser.add_argument("--backend", choices=("mlx", "faster-whisper"), default="mlx",
                        help="motor de transcrição (padrão: mlx)")
    args = parser.parse_args()
    base = Path(args.output) if args.output else None
    if args.output_dir:
        base = Path(args.output_dir) / Path(args.entrada).stem
    try:
        model = args.model or (WINDOWS_MODEL if args.backend == "faster-whisper" else MODEL)
        transcribe(args.entrada, base, model, args.language, args.backend)
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
