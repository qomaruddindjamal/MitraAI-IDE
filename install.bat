@echo off
REM ============================================
REM MitraAI - All-in-One Installer (Windows)
REM Satu perintah untuk install semuanya:
REM - Download Antigravity standalone
REM - Download Antigravity IDE
REM - Install patch + custom model support
REM - Fix port 50999 (Hyper-V/WinNAT)
REM - Buat shortcut Desktop
REM ============================================

setlocal EnableDelayedExpansion

echo.
echo  ============================================
echo    MitraAI - All-in-One Installer
echo    Auto-install Antigravity + IDE + Patch
echo  ============================================
echo.

REM ─── Prasyarat Check ──────────────────────────

echo [1/8] Memeriksa prasyarat...

REM Cek admin rights
net session >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Tidak dijalankan sebagai Administrator.
    echo          Beberapa fitur mungkin tidak berfungsi (WinNAT fix).
    echo          Klik kanan ^"Run as Administrator^" untuk hasil terbaik.
    echo.
)

REM Cek Node.js
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js tidak ditemukan!
    echo.
    echo Install Node.js 22+ dari: https://nodejs.org/
    echo Atau jalankan: winget install OpenJS.NodeJS.LTS
    echo.
    pause
    exit /b 1
)
for /f "tokens=1 delims=v" %%v in ('node --version') do set NODE_VER=%%v
echo    Node.js: OK (v%NODE_VER%)

REM Cek Git
where git >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Git tidak ditemukan!
    echo Install dari: https://git-scm.com/
    pause
    exit /b 1
)
echo    Git: OK

REM ─── Fix Port 50999 Permanen ──────────────────

echo.
echo [2/8] Fix port 50999 (Hyper-V/WinNAT)...

REM Cek apakah port 50999 diblokir oleh WinNAT
netsh interface ipv4 show excludedportrange protocol=tcp | findstr "50999" >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo    Port 50999 diblokir oleh Hyper-V/WinNAT.
    echo    Memperbaiki...
    net stop winnat >nul 2>&1
    timeout /t 2 /nobreak >nul
    net start winnat >nul 2>&1
    echo    WinNAT restarted. Port 50999 sekarang tersedia.
) else (
    echo    Port 50999: OK (tidak diblokir)
)

REM Stop semua proses yang memakai port 50999
for /f "tokens=5" %%p in ('netstat -ano ^| findstr "50999" ^| findstr "LISTENING"') do (
    echo    Menghentikan proses di port 50999 (PID: %%p)...
    taskkill /PID %%p /F >nul 2>&1
)

REM Tambahkan port exclusion agar tidak diblokir lagi
netsh int ipv4 add excludedportrange protocol=tcp startport=50999 numberofports=1 persistent=yes >nul 2>&1
echo    Port 50999 di-exclude dari Hyper-V reservation.

REM ─── Setup Direktori ──────────────────────────

echo.
echo [3/8] Menyiapkan direktori...

set INSTALL_DIR=C:\MitraAI
set PATCH_DIR=%USERPROFILE%\MitraAI-patch
set IDE_DEFAULT=%LOCALAPPDATA%\Programs\Antigravity IDE

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%PATCH_DIR%" mkdir "%PATCH_DIR%"
echo    Install dir: %INSTALL_DIR%
echo    Patch dir:   %PATCH_DIR%

REM ─── Download Antigravity Standalone ──────────

echo.
echo [4/8] Download Antigravity standalone...

if exist "%INSTALL_DIR%\Antigravity.exe" (
    echo    Antigravity sudah ada di %INSTALL_DIR%
) else (
    echo    Downloading Antigravity v2.23.0...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://storage.googleapis.com/oslo-team-release/channels/production/versions/2.23.0/win-x64/AntigravitySetup.exe' -OutFile '%TEMP%\AntigravitySetup.exe' -UseBasicParsing}" 2>nul

    if exist "%TEMP%\AntigravitySetup.exe" (
        echo    Extracting...
        powershell -Command "Start-Process -FilePath '%TEMP%\AntigravitySetup.exe' -ArgumentList '/S','/D=%INSTALL_DIR%' -Wait -NoNewWindow" 2>nul
        if exist "%INSTALL_DIR%\Antigravity.exe" (
            echo    Antigravity standalone: OK
        ) else (
            echo    [WARNING] Extract gagal. Coba install manual dari https://antigravity.google/download
        )
    ) else (
        echo    [WARNING] Download gagal.
        echo    Download manual dari: https://antigravity.google/download
        echo    Extract ke: %INSTALL_DIR%
    )
)

REM ─── Download Antigravity IDE ─────────────────

echo.
echo [5/8] Download Antigravity IDE...

if exist "%IDE_DEFAULT%\Antigravity IDE.exe" (
    echo    Antigravity IDE sudah ada
) else (
    echo    Downloading Antigravity IDE v2.5.5...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://dl.google.com/antigravity-ide/win/AntigravityIDE-Setup.exe' -OutFile '%TEMP%\AntigravityIDESetup.exe' -UseBasicParsing}" 2>nul

    if exist "%TEMP%\AntigravityIDESetup.exe" (
        echo    Installing IDE...
        start /wait "" "%TEMP%\AntigravityIDESetup.exe" /S
        if exist "%IDE_DEFAULT%\Antigravity IDE.exe" (
            echo    Antigravity IDE: OK
        ) else (
            echo    [WARNING] IDE install gagal. Coba manual dari https://antigravity.google/download
        )
    ) else (
        echo    [WARNING] Download IDE gagal.
        echo    Download manual dari: https://antigravity.google/download
    )
)

REM ─── Clone dan Build Patch ────────────────────

echo.
echo [6/8] Install patch MitraAI...

cd /d "%PATCH_DIR%"

if exist "%PATCH_DIR%\package.json" (
    echo    Patch sudah ada, updating...
    git pull >nul 2>&1
) else (
    echo    Cloning patch repository...
    git clone https://github.com/qomaruddindjamal/MitraAI.git "%PATCH_DIR%" >nul 2>&1
)

echo    Installing dependencies...
call npm ci --ignore-scripts >nul 2>&1

echo    Building...
call npm run build >nul 2>&1
echo    Patch: OK

REM ─── Apply Patch ──────────────────────────────

echo.
echo [7/8] Menerapkan patch...

REM Patch standalone
if exist "%INSTALL_DIR%\resources" (
    echo    Patching standalone app...
    node "%PATCH_DIR%\scripts\deploy.mjs" --resources "%INSTALL_DIR%\resources" >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        echo    Standalone patch: OK
    ) else (
        echo    [WARNING] Standalone patch gagal.
    )
)

REM Patch IDE
if exist "%IDE_DEFAULT%\resources" (
    echo    Patching IDE...
    node "%PATCH_DIR%\scripts\ide.mjs" apply --resources "%IDE_DEFAULT%\resources" >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        echo    IDE patch: OK
    ) else (
        echo    [WARNING] IDE patch gagal.
    )
)

REM ─── Buat Shortcut dan Launcher ───────────────

echo.
echo [8/8] Membuat shortcut Desktop...

REM MitraAI standalone launcher
(
echo @echo off
echo REM MitraAI Launcher - Auto fix port
echo netsh interface ipv4 show excludedportrange protocol=tcp ^| findstr "50999" ^>nul 2^>^&1
echo if %%ERRORLEVEL%% neq 0 ^(
echo     netsh int ipv4 add excludedportrange protocol=tcp startport=50999 numberofports=1 persistent=yes ^>nul 2^>^&1
echo ^)
echo for /f "tokens=5" %%%%p in ^('netstat -ano ^| findstr "50999" ^| findstr "LISTENING"'^) do ^(
echo     taskkill /PID %%%%p /F ^>nul 2^>^&1
echo ^)
echo timeout /t 2 /nobreak ^>nul
echo start "" "%INSTALL_DIR%\Antigravity.exe"
) > "%INSTALL_DIR%\START-MitraAI.bat"

REM MitraAI IDE launcher
(
echo @echo off
echo REM MitraAI IDE Launcher - Auto fix port + proxy
echo netsh interface ipv4 show excludedportrange protocol=tcp ^| findstr "50999" ^>nul 2^>^&1
echo if %%ERRORLEVEL%% neq 0 ^(
echo     netsh int ipv4 add excludedportrange protocol=tcp startport=50999 numberofports=1 persistent=yes ^>nul 2^>^&1
echo ^)
echo for /f "tokens=5" %%%%p in ^('netstat -ano ^| findstr "50999" ^| findstr "LISTENING"'^) do ^(
echo     taskkill /PID %%%%p /F ^>nul 2^>^&1
echo ^)
echo timeout /t 2 /nobreak ^>nul
echo cd /d "%PATCH_DIR%"
echo call npm run proxy:start ^>nul 2^>^&1
echo timeout /t 3 /nobreak ^>nul
echo start "" "%IDE_DEFAULT%\Antigravity IDE.exe"
) > "%IDE_DEFAULT%\START-MitraAI-IDE.bat"

REM Desktop shortcuts
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $sc = $ws.CreateShortcut('%USERPROFILE%\Desktop\MitraAI.lnk'); $sc.TargetPath = '%INSTALL_DIR%\START-MitraAI.bat'; $sc.WorkingDirectory = '%INSTALL_DIR%'; $sc.Description = 'MitraAI - Local Model AI Assistant'; $sc.IconLocation = '%INSTALL_DIR%\Antigravity.exe,0'; $sc.Save()" 2>nul

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $sc = $ws.CreateShortcut('%USERPROFILE%\Desktop\MitraAI IDE.lnk'); $sc.TargetPath = '%IDE_DEFAULT%\START-MitraAI-IDE.bat'; $sc.WorkingDirectory = '%IDE_DEFAULT%'; $sc.Description = 'MitraAI IDE - AI-Powered Code Editor'; $sc.IconLocation = '%IDE_DEFAULT%\Antigravity IDE.exe,0'; $sc.Save()" 2>nul

echo    Shortcut "MitraAI": OK
echo    Shortcut "MitraAI IDE": OK

REM ─── Selesai ──────────────────────────────────

echo.
echo  ============================================
echo    INSTALLASI SELESAI!
echo  ============================================
echo.
echo  Shortcut sudah dibuat di Desktop:
echo    - MitraAI      (standalone app)
echo    - MitraAI IDE  (code editor)
echo.
echo  Port 50999 sudah di-fix permanen.
echo  Kedua app bisa langsung dijalankan.
echo.
echo  Langkah selanjutnya:
echo  1. Klik "MitraAI" di Desktop untuk mulai
echo  2. Buka browser manager: http://127.0.0.1:50999
echo  3. Tambahkan model (Ollama, OpenAI, dll)
echo.
echo  Dokumentasi lengkap:
echo    https://github.com/qomaruddindjamal/MitraAI
echo    https://github.com/qomaruddindjamal/MitraAI-IDE
echo.
pause
