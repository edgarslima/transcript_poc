import contextlib
import io
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import transcribe


class TranscriptionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.source = self.directory / 'entrada.v1.mov'
        self.source.touch()

    def test_timestamps(self):
        self.assertEqual(transcribe._ts(3661.25), '01:01:01,250')
        self.assertEqual(transcribe._ts(0), '00:00:00,000')

    def test_missing_file_fails_before_loading_model(self):
        with self.assertRaises(FileNotFoundError):
            transcribe.transcribe(str(self.directory / 'missing.wav'))

    def test_mlx_writes_text_and_subtitles_with_default_name(self):
        engine = types.ModuleType('mlx_whisper')
        engine.transcribe = mock.Mock(return_value={
            'text': 'Olá mundo',
            'segments': [{'start': 1, 'end': 2.5, 'text': ' Olá mundo '}],
        })
        with mock.patch.dict(sys.modules, {'mlx_whisper': engine}), \
             mock.patch.object(transcribe, 'DEFAULT_OUTPUT_DIR', self.directory / 'output'), \
             contextlib.redirect_stdout(io.StringIO()):
            transcribe.transcribe(str(self.source))
        engine.transcribe.assert_called_once_with(
            str(self.source.resolve()), path_or_hf_repo=transcribe.MODEL, language='pt')
        self.assertEqual((self.directory / 'output/entrada.v1.txt').read_text(encoding='utf-8'), 'Olá mundo')
        self.assertEqual((self.directory / 'output/entrada.v1.srt').read_text(encoding='utf-8'),
                         '1\n00:00:01,000 --> 00:00:02,500\nOlá mundo\n\n')

    def test_faster_whisper_uses_options_and_writes_segments(self):
        engine = types.ModuleType('faster_whisper')
        segment = types.SimpleNamespace(text=' Hello', start=0, end=1)
        model = mock.Mock()
        model.transcribe.return_value = (iter([segment]), None)
        engine.WhisperModel = mock.Mock(return_value=model)
        base = self.directory / 'nested' / 'custom.name'
        with mock.patch.dict(sys.modules, {'faster_whisper': engine}), contextlib.redirect_stdout(io.StringIO()):
            transcribe.transcribe(str(self.source), base, 'small', 'en', 'faster-whisper')
        engine.WhisperModel.assert_called_once_with('small', device='cpu', compute_type='int8')
        model.transcribe.assert_called_once_with(str(self.source.resolve()), language='en')
        self.assertEqual(Path(f'{base}.txt').read_text(encoding='utf-8'), 'Hello')
        self.assertIn('00:00:00,000 --> 00:00:01,000', Path(f'{base}.srt').read_text(encoding='utf-8'))

    def test_main_selects_backend_model_and_output_dir(self):
        args = ['transcribe.py', '--backend', 'faster-whisper', '-d', 'results', str(self.source)]
        with mock.patch.object(sys, 'argv', args), mock.patch.object(transcribe, 'transcribe') as run:
            self.assertEqual(transcribe.main(), 0)
        run.assert_called_once_with(str(self.source), Path('results/entrada.v1'), 'large-v3', 'pt', 'faster-whisper')

    def test_main_reports_runtime_errors(self):
        with mock.patch.object(sys, 'argv', ['transcribe.py', 'missing.wav']), \
             contextlib.redirect_stderr(io.StringIO()) as error:
            self.assertEqual(transcribe.main(), 1)
        self.assertIn('Arquivo de entrada não encontrado', error.getvalue())

    def test_output_options_are_mutually_exclusive(self):
        with mock.patch.object(sys, 'argv', ['transcribe.py', 'input.wav', '-o', 'x', '-d', 'y']), \
             contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                transcribe.main()
        self.assertEqual(error.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
