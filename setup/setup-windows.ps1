<#
  Reel Studio set-up for Windows 10/11.
  Checks Python 3.10+ and FFmpeg (installs them with winget if you say yes), makes a private Python environment
  (.venv) with the two packages Reel Studio needs, and puts a "Reel Studio" shortcut on the Desktop and in Start.

  Double-click "Set up Reel Studio.bat", or run:  powershell -ExecutionPolicy Bypass -File setup\setup-windows.ps1
  Options:  -Yes  (don't ask, install what's missing)   -NoShortcuts  (skip the Desktop / Start shortcuts)
  Safe to run again: it only adds what's missing.
#>
param([switch]$Yes, [switch]$NoShortcuts)
$ErrorActionPreference = 'Stop'
$App = Split-Path -Parent $PSScriptRoot

function Say($t) { Write-Host ''; Write-Host "== $t" -ForegroundColor Cyan }
function Ok($t) { Write-Host "   $t" -ForegroundColor Green }
function Ask($q) {
    if ($Yes) { return $true }
    $a = Read-Host "   $q [Y/n]"
    return ($a -eq '' -or $a -match '^[Yy]')
}
function Refresh-Path {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
}
function Python-Ok($exe, $pre) {
    try {
        $v = & $exe @pre -c "import sys; print('%d.%d' % sys.version_info[:2]); sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>$null
        return ($LASTEXITCODE -eq 0 -and $v)
    } catch { return $false }
}
function Find-Python {
    $cands = @(
        @{ exe = 'py'; pre = @('-3') },
        @{ exe = 'python'; pre = @() },
        @{ exe = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"; pre = @() },
        @{ exe = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"; pre = @() },
        @{ exe = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"; pre = @() }
    )
    foreach ($c in $cands) {
        if ((Get-Command $c.exe -ErrorAction SilentlyContinue) -and (Python-Ok $c.exe $c.pre)) { return $c }
    }
    return $null
}
function Find-FFmpeg {
    $f = Get-Command ffmpeg -ErrorAction SilentlyContinue
    if ($f) { return $f.Source }
    $g = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter ffmpeg.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($g) { return $g.FullName }
    return $null
}
function Have-Winget { return [bool](Get-Command winget -ErrorAction SilentlyContinue) }

Write-Host 'Reel Studio set-up' -ForegroundColor White
Write-Host "Folder: $App"

# 1. Python ------------------------------------------------------------------------------------------
Say 'Python 3.10 or newer'
$py = Find-Python
if (-not $py) {
    if (-not (Have-Winget)) { throw 'Python is missing and winget is not available. Install Python 3.12 from https://www.python.org/downloads/ (tick "Add python.exe to PATH"), then run this again.' }
    if (-not (Ask 'Python is not installed. Install Python 3.12 now (about 30 MB)?')) { throw 'Python is needed. Stopped.' }
    winget install -e --id Python.Python.3.12 --scope user --accept-package-agreements --accept-source-agreements --disable-interactivity
    Refresh-Path
    $py = Find-Python
    if (-not $py) { throw 'Python was installed but is not found yet. Close this window, then run the set-up again.' }
}
Ok ("Python found: " + $py.exe + ' ' + ($py.pre -join ' '))

# 2. FFmpeg ------------------------------------------------------------------------------------------
Say 'FFmpeg (cuts and exports the video)'
$ff = Find-FFmpeg
if (-not $ff) {
    if (-not (Have-Winget)) { throw 'FFmpeg is missing and winget is not available. Install the "full" build from https://www.gyan.dev/ffmpeg/builds/ and add its bin folder to PATH, then run this again.' }
    if (-not (Ask 'FFmpeg is not installed. Install it now (about 100 MB)?')) { throw 'FFmpeg is needed. Stopped.' }
    winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements --disable-interactivity
    Refresh-Path
    $ff = Find-FFmpeg
    if (-not $ff) { throw 'FFmpeg was installed but is not found yet. Close this window, then run the set-up again.' }
}
$filters = & $ff -hide_banner -filters 2>$null | Out-String
if ($filters -notmatch '\scas\s' -or $filters -notmatch '\slut3d\s') { Write-Host '   Note: this FFmpeg lacks the "cas" or "lut3d" filter. Sharpened 2K/4K exports may fail; the "full" build has them.' -ForegroundColor Yellow }
Ok "FFmpeg found: $ff"

# 3. Private Python environment + packages --------------------------------------------------------------
Say 'Python packages (Pillow, NumPy) in a private environment'
$venvPy = Join-Path $App '.venv\Scripts\python.exe'
if (-not (Test-Path $venvPy)) {
    $pre = $py.pre
    & $py.exe @pre -m venv (Join-Path $App '.venv')
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the Python environment (.venv).' }
}
& $venvPy -m pip install --disable-pip-version-check --quiet -r (Join-Path $App 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Installing the Python packages failed (is the internet connection on?).' }
Ok 'Packages ready (.venv)'

# 4. Shortcuts --------------------------------------------------------------------------------------------
if (-not $NoShortcuts) {
    Say 'Shortcuts'
    $sh = New-Object -ComObject WScript.Shell
    $targets = @([Environment]::GetFolderPath('Desktop'), (Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs'))
    foreach ($dir in $targets) {
        $lnk = $sh.CreateShortcut((Join-Path $dir 'Reel Studio.lnk'))
        $lnk.TargetPath = Join-Path $App 'Start Reel Studio.bat'
        $lnk.WorkingDirectory = $App
        $lnk.IconLocation = (Join-Path $App 'setup\reel-studio.ico') + ',0'
        $lnk.Description = 'Make reels from your own clips'
        $lnk.Save()
    }
    Ok 'Reel Studio is on your Desktop and in the Start menu'
}

# Remember where Reel Studio lives, so Claude's Reel Studio plugin can find it from any folder
[IO.File]::WriteAllText((Join-Path $env:USERPROFILE '.reel-studio'), $App)

Say 'Done'
Write-Host '   Start Reel Studio from its shortcut (or "Start Reel Studio.bat"). Your browser opens and asks for your footage folder.'
Write-Host '   Keep the black Reel Studio window open while you edit.'
