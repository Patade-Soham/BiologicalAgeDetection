$ErrorActionPreference = "Stop"

$root = "external_models"
New-Item -ItemType Directory -Path $root -Force | Out-Null

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git command not found"
}

if (-not (Test-Path "$root\AGE")) {
    git clone https://github.com/gitliber/AGE "$root\AGE"
}

if (-not (Test-Path "$root\inaFaceAnalyzer")) {
    git clone https://github.com/ina-foss/inaFaceAnalyzer "$root\inaFaceAnalyzer"
}

Write-Host "External model repositories are available under $root"
