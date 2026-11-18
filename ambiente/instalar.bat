
@echo off
setlocal
cd /d "%~dp0.."

echo =====================================
echo      FaceAccess - Instalacao
echo =====================================

py --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.12 nao encontrado.
    echo Instale o Python 3.12 e tente novamente.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    py -m venv .venv
    if errorlevel 1 goto erro
)

".venv\Scripts\python.exe" -m pip install -r "ambiente\requirements.txt"
if errorlevel 1 goto erro

echo.
echo Instalacao concluida com sucesso!
pause
exit /b 0

:erro
echo.
echo Erro na instalacao.
pause
exit /b 1
