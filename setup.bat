@echo off
REM ============================================
REM MitraAI IDE - Setup Script (Windows)
REM Membuat shortcut di Desktop setelah install
REM ============================================

echo ========================================
echo   MitraAI IDE - Setup
echo ========================================
echo.

REM Cek Node.js
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Node.js tidak ditemukan.
    echo Install dari https://nodejs.org/
    pause
    exit /b 1
)

REM Install dependencies
echo Menginstall dependencies...
call npm ci --ignore-scripts
if %ERRORLEVEL% neq 0 (
    echo ERROR: npm ci gagal
    pause
    exit /b 1
)

REM Build
echo Building project...
call npm run build
if %ERRORLEVEL% neq 0 (
    echo ERROR: Build gagal
    pause
    exit /b 1
)

REM Deteksi path Antigravity IDE
set IDE_PATH=
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Antigravity IDE\Antigravity IDE.exe" (
    set IDE_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Antigravity IDE
)
if exist "C:\Program Files\Antigravity IDE\Antigravity IDE.exe" (
    set IDE_PATH=C:\Program Files\Antigravity IDE
)

if "%IDE_PATH%"=="" (
    echo.
    echo WARNING: Antigravity IDE tidak ditemukan di lokasi default.
    echo Download dari https://antigravity.google/download
    echo.
    echo Shortcut akan dibuat tapi perlu edit manual setelah IDE terinstall.
)

REM Buat shortcut di Desktop
echo Membuat shortcut di Desktop...
if not "%IDE_PATH%"=="" (
    powershell -Command "$ws = New-Object -ComObject WScript.Shell; $sc = $ws.CreateShortcut('%USERPROFILE%\Desktop\MitraAI IDE.lnk'); $sc.TargetPath = '%IDE_PATH%\Antigravity IDE.exe'; $sc.WorkingDirectory = '%IDE_PATH%'; $sc.Description = 'MitraAI IDE - AI-Powered Code Editor'; $sc.Save()"
) else (
    powershell -Command "$ws = New-Object -ComObject WScript.Shell; $sc = $ws.CreateShortcut('%USERPROFILE%\Desktop\MitraAI IDE.lnk'); $sc.TargetPath = '%~dp0START-MitraAI-IDE.bat'; $sc.WorkingDirectory = '%~dp0'; $sc.Description = 'MitraAI IDE - AI-Powered Code Editor'; $sc.Save()"
)

REM Terapkan patch IDE jika IDE ditemukan
if not "%IDE_PATH%"=="" (
    echo.
    echo Menerapkan patch IDE...
    call npm run ide:check -- --resources "%IDE_PATH%\resources"
    call npm run ide:apply -- --resources "%IDE_PATH%\resources"
)

echo.
echo ========================================
echo   Setup selesai!
echo ========================================
echo.
echo Shortcut "MitraAI IDE" sudah dibuat di Desktop.
echo.
echo Langkah selanjutnya:
echo 1. Start proxy: npm run proxy:start -- --open
echo 2. Tambahkan model di browser manager
echo 3. Klik shortcut "MitraAI IDE" di Desktop
echo.
pause
