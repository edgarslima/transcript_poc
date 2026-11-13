param(
    [Parameter(Position = 0)]
    [string]$Entrada,
    [Alias('o')][string]$Output,
    [Alias('d')][string]$OutputDir,
    [Alias('m')][string]$Model,
    [Alias('l')][string]$Language,
    [string]$Python,
    [Alias('h')][switch]$Help
)

$ErrorActionPreference = 'Stop'
if (-not $Python) { $Python = $env:PYTHON }
if (-not $Python) {
    if ($env:VIRTUAL_ENV -and (Test-Path -LiteralPath (Join-Path $env:VIRTUAL_ENV 'Scripts\python.exe') -PathType Leaf)) {
        $Python = Join-Path $env:VIRTUAL_ENV 'Scripts\python.exe'
    } elseif (Test-Path -LiteralPath (Join-Path $PSScriptRoot '.venv\Scripts\python.exe') -PathType Leaf) {
        $Python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
    } elseif (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'venv\Scripts\python.exe') -PathType Leaf) {
        $Python = Join-Path $PSScriptRoot 'venv\Scripts\python.exe'
    } else {
        $Python = 'python'
    }
}

if ($Help) {
    Write-Output 'Uso: .\transcript.ps1 [-Entrada] ARQUIVO [-Output CAMINHO | -OutputDir PASTA] [-Model MODELO] [-Language IDIOMA] [-Python CAMINHO]'
    Write-Output 'Abreviações: -o, -d, -m, -l e -h. Consulte transcript_doc_ps.md para exemplos.'
    exit 0
}
if (-not $Entrada) {
    [Console]::Error.WriteLine('ERRO: informe o arquivo de entrada. Use -Help para obter ajuda.')
    exit 1
}
if ($Output -and $OutputDir) {
    [Console]::Error.WriteLine('ERRO: use -Output ou -OutputDir, não ambos.')
    exit 1
}

$Argumentos = @((Join-Path $PSScriptRoot 'transcribe.py'), '--backend', 'faster-whisper')
if ($Output) { $Argumentos += @('--output', $Output) }
if ($OutputDir) { $Argumentos += @('--output-dir', $OutputDir) }
if ($Model) { $Argumentos += @('--model', $Model) }
if ($Language) { $Argumentos += @('--language', $Language) }
$Argumentos += @('--', $Entrada)
try {
    & $Python @Argumentos
    exit $LASTEXITCODE
} catch {
    [Console]::Error.WriteLine("ERRO ao executar Python: $_")
    exit 1
}
