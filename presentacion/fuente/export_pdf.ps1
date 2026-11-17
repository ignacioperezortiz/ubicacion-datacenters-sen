param([string]$pptx, [string]$pdf)
$ErrorActionPreference = 'Stop'
$pptx = (Resolve-Path $pptx).Path
$pp = New-Object -ComObject PowerPoint.Application
try {
  $pres = $pp.Presentations.Open($pptx, -1, 0, 0)
  $pres.SaveAs($pdf, 32)   # ppSaveAsPDF
  $pres.Close()
} finally {
  # cerrar PowerPoint solo si no quedó ninguna otra presentación abierta (puede estar en uso)
  if ($pp.Presentations.Count -eq 0) { $pp.Quit() }
  [System.Runtime.Interopservices.Marshal]::ReleaseComObject($pp) | Out-Null
}
Write-Output "pdf: $pdf"
