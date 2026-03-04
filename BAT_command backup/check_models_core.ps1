Write-Host "========================================" 
Write-Host " [1/2] LLaMA.cpp (llama-server) Models" -ForegroundColor Cyan 
Write-Host "========================================" 
$procs = Get-Process -Name 'llama-server' -ErrorAction SilentlyContinue 
if ($procs) { 
  foreach ($p in $procs) { 
    $ws = [double]($p | Select-Object -ExpandProperty WorkingSet64)
    $p | Add-Member -NotePropertyName 'Memory(MB)' -NotePropertyValue [math]::Round($ws / 1MB, 2) -Force
    $cmd = ""
    try {
        $cmd = (Get-CimInstance Win32_Process -Filter ('ProcessId = ' + $p.Id) -ErrorAction SilentlyContinue).CommandLine 
    } catch {}
    
    $model = 'Unknown' 
    if ($cmd -match '-m\s+["'']?([^"'' ]+\.gguf)["'']?') { 
      $fullPath = $matches[1] 
      $model = Split-Path $fullPath -Leaf 
    } 
    $p | Add-Member -NotePropertyName 'Model_Name' -NotePropertyValue $model -Force
  } 
  $procs | Sort-Object -Descending 'Memory(MB)' | Select-Object Id, 'Memory(MB)', Model_Name | Format-Table -AutoSize 
} else { 
  Write-Host "No llama-server process found." -ForegroundColor Yellow 
} 

Write-Host "" 
Write-Host "========================================" 
Write-Host " [2/2] Ollama Models (Active in Memory)" -ForegroundColor Cyan 
Write-Host "========================================" 
try { 
  $resp = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/ps' -ErrorAction Stop 
  if ($resp.models -and $resp.models.Count -gt 0) { 
    $resp.models | Select-Object name, @{Name='Total_Size(MB)';Expression={[math]::Round([double]$_.size / 1MB, 2)}}, @{Name='VRAM(MB)';Expression={[math]::Round([double]$_.size_vram / 1MB, 2)}} | Format-Table -AutoSize 
  } else { 
    Write-Host "Ollama service is running, but no models are currently active." -ForegroundColor Yellow 
  } 
} catch { 
  Write-Host "Cannot connect to Ollama service (Not running or wrong port)." -ForegroundColor Red 
}
