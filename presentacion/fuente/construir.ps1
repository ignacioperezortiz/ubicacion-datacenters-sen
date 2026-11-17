# Arma la presentación: texto y layout (build.js) -> ecuaciones nativas (eq\ecuaciones.py) -> PDF (PowerPoint).
# No recalcula cifras, gráficos ni anexos: para eso está ..\regenerar.ps1.
param(
  [string]$Salida = (Join-Path (Split-Path $PSScriptRoot -Parent) "Presentacion de avance - Ubicacion de data centers en el SEN.pptx"),
  [string]$Python = "python",
  [switch]$SinPdf
)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$Salida = [System.IO.Path]::GetFullPath($Salida)
New-Item -ItemType Directory -Force (Split-Path $Salida -Parent) | Out-Null

# Módulos de Node del propio repositorio (package.json fija pptxgenjs 4.0.1 y jszip 3.10.2).
$NodeModules = Join-Path $PSScriptRoot "node_modules"
if (-not (Test-Path (Join-Path $NodeModules "pptxgenjs"))) {
  Write-Output "Instalando los módulos de Node (npm ci)..."
  # npm escribe avisos («npm notice», «npm warn») en stderr. Con 'Stop', Windows PowerShell 5.1 los convierte
  # en error si la salida está redirigida (p. ej., al correr desde otro programa), así que aquí solo cuenta el código de salida.
  $ErrorActionPreference = 'Continue'
  npm ci --no-audit --no-fund 2>&1 | ForEach-Object { "$_" }
  $codigoNpm = $LASTEXITCODE
  $ErrorActionPreference = 'Stop'
  if ($codigoNpm -ne 0) { throw "npm ci falló; corra 'npm install' en $PSScriptRoot" }
}
$env:NODE_PATH = $NodeModules

node build.js $Salida
if ($LASTEXITCODE -ne 0) { throw "build.js falló" }
& $Python eq\ecuaciones.py $Salida "$Salida.eqs.json"
if ($LASTEXITCODE -ne 0) { throw "ecuaciones.py falló" }
Remove-Item "$Salida.eqs.json"
if (-not $SinPdf) {
  & (Join-Path $PSScriptRoot "export_pdf.ps1") $Salida ([System.IO.Path]::ChangeExtension($Salida, ".pdf"))
}
