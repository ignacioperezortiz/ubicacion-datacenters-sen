param([string]$pptx, [string]$outdir)
$ErrorActionPreference = 'Stop'
$pptx = (Resolve-Path $pptx).Path
New-Item -ItemType Directory -Force $outdir | Out-Null
$outdir = (Resolve-Path $outdir).Path
Get-ChildItem $outdir -Filter *.png | Remove-Item -Force
$pp = New-Object -ComObject PowerPoint.Application
try {
  $pres = $pp.Presentations.Open($pptx, -1, 0, 0)   # ReadOnly, not Untitled, no window
  $i = 1
  foreach ($sl in $pres.Slides) { $sl.Export((Join-Path $outdir ("slide-{0:D2}.png" -f $i)), "PNG", 1600, 900); $i++ }
  $pres.Close()
} finally {
  # cerrar PowerPoint solo si no quedó ninguna otra presentación abierta (puede estar en uso)
  if ($pp.Presentations.Count -eq 0) { $pp.Quit() }
  [System.Runtime.Interopservices.Marshal]::ReleaseComObject($pp) | Out-Null
}
Write-Output "exported $($i-1) slides to $outdir"
