[CmdletBinding()]
param(
    [switch]$SkipAssembly,
    [string]$PythonCommand = 'python',
    [string]$CompilerCommand = 'tectonic',
    [string]$CacheDirectory
)

$ErrorActionPreference = 'Stop'
$BuildArguments = @((Join-Path $PSScriptRoot 'build_book.py'), '--compiler', $CompilerCommand)
if ($SkipAssembly) { $BuildArguments += '--skip-assembly' }
if ($CacheDirectory) { $BuildArguments += @('--cache-dir', $CacheDirectory) }
& $PythonCommand @BuildArguments
if ($LASTEXITCODE -ne 0) { throw "Book build failed with exit code $LASTEXITCODE." }
