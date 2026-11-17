# Regenera toda la presentación desde los resultados del repositorio (casos\ y resultados\tablas\).
#
#   .\regenerar.ps1                      # todo: cifras, gráficos, anexos, PPTX y PDF en esta carpeta
#   .\regenerar.ps1 -SinAnexos           # deja los anexos 10/20/30 como están (p. ej. si los casos no son los de inicio 2025)
#   .\regenerar.ps1 -Salida C:\tmp\x.pptx  # escribe el PPTX y el PDF en otra parte
#
# Pasos:
#   1. fuente\extraer_cifras.py              -> fuente\cifras.json (cifras de casos y resultados)
#   2. fuente\graficos\mapa_dc_2050_fig.py   -> fuente\graficos\mapa_dc_2050.png (descarga GADM si falta)
#   3. fuente\graficos\diagrama_red.py       -> fuente\graficos\diagrama_red.png
#   4. fuente\anexos\anexo_generacion.py     -> fuente\anexos\10_generacion.js
#   5. fuente\anexos\anexos_tx_dc.py         -> fuente\anexos\20_transmision.js, 30_data_centers.js
#   6. fuente\construir.ps1                  -> PPTX con ecuaciones nativas y PDF
# 40_modelo.js y FORMATO.md se escriben a mano; ningún paso los toca.
param(
  [string]$Salida = (Join-Path $PSScriptRoot "Presentacion de avance - Ubicacion de data centers en el SEN.pptx"),
  [string]$Python = "python",
  [switch]$SinAnexos,
  [switch]$SinPdf
)
$ErrorActionPreference = 'Stop'
$F = Join-Path $PSScriptRoot "fuente"
$env:PYTHONIOENCODING = "utf-8"

function Paso([string]$titulo, [string[]]$argumentos) {
  Write-Output ""
  Write-Output "=== $titulo"
  & $Python @argumentos
  if ($LASTEXITCODE -ne 0) { throw "Falló: $titulo" }
}

Paso "1/6 Cifras de casos y resultados (cifras.json)" @("-B", (Join-Path $F "extraer_cifras.py"))
Paso "2/6 Mapa de data centers 2050" @("-B", (Join-Path $F "graficos\mapa_dc_2050_fig.py"))
Paso "3/6 Diagrama de la red" @("-B", (Join-Path $F "graficos\diagrama_red.py"))
if ($SinAnexos) {
  Write-Output ""
  Write-Output "=== 4-5/6 Anexos: se omiten (-SinAnexos); se usan los .js que ya están en fuente\anexos"
} else {
  Paso "4/6 Anexo de generación (10_generacion.js)" @("-B", (Join-Path $F "anexos\anexo_generacion.py"))
  Paso "5/6 Anexos de transmisión y data centers (20_transmision.js, 30_data_centers.js)" @("-B", (Join-Path $F "anexos\anexos_tx_dc.py"))
}
Write-Output ""
Write-Output "=== 6/6 PPTX, ecuaciones y PDF"
$args6 = @{ Salida = $Salida; Python = $Python }
if ($SinPdf) { $args6.SinPdf = $true }
& (Join-Path $F "construir.ps1") @args6
Write-Output ""
Write-Output "Listo: $Salida"
