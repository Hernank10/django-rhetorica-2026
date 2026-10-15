param([string]$Path)
$full = (Resolve-Path $Path).Path
$content = [System.IO.File]::ReadAllText($full)
$utf8SinBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($full, $content, $utf8SinBom)
Write-Host "[OK] BOM removido de $Path"