import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class ScriptTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.source = self.directory / 'arquivo com espacos.mov'
        self.source.touch()
        (self.directory / 'mlx_whisper.py').write_text(
            "def transcribe(path, path_or_hf_repo, language):\n"
            "    return {'text': language, 'segments': []}\n", encoding='utf-8')
        (self.directory / 'faster_whisper.py').write_text(
            "from types import SimpleNamespace\n"
            "class WhisperModel:\n"
            "    def __init__(self, model, device, compute_type): pass\n"
            "    def transcribe(self, path, language):\n"
            "        return iter([SimpleNamespace(text=language, start=0, end=1)]), None\n", encoding='utf-8')
        self.env = dict(os.environ, PYTHONPATH=str(self.directory))

    @unittest.skipUnless(shutil.which('bash'), 'bash não disponível')
    def test_shell_forwards_arguments(self):
        base = self.directory / 'shell output' / 'transcricao'
        result = subprocess.run(['bash', str(ROOT / 'transcript.sh'), '--python', sys.executable,
                                 '-o', str(base), '-l', 'en', str(self.source)],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(Path(f'{base}.txt').read_text(encoding='utf-8'), 'en')

    @unittest.skipUnless(shutil.which('pwsh') or shutil.which('powershell'), 'PowerShell não disponível')
    def test_powershell_forwards_arguments(self):
        base = self.directory / 'powershell output' / 'transcricao'
        shell = shutil.which('pwsh') or shutil.which('powershell')
        result = subprocess.run([shell, '-NoProfile', '-File', str(ROOT / 'transcript.ps1'),
                                 str(self.source), '-Python', sys.executable,
                                 '-Output', str(base), '-Language', 'en'],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(Path(f'{base}.txt').read_text(encoding='utf-8'), 'en')


if __name__ == '__main__':
    unittest.main()
