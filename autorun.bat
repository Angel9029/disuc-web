@echo off
title DISUC WEB
cd /d "%~dp0"

echo ========================================
echo      Iniciando DISUC WEB
echo ========================================
echo.

:: Verificar si existe el entorno virtual
if not exist ".venv\Scripts\activate.bat" (
    echo [+] Creando entorno virtual...
    python -m venv .venv

    if errorlevel 1 (
        echo.
        echo [ERROR] No se pudo crear el entorno virtual.
        pause
        exit /b
    )

    echo.
    echo [+] Instalando dependencias...
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt

    if errorlevel 1 (
        echo.
        echo [ERROR] No se pudieron instalar las dependencias.
        pause
        exit /b
    )
) else (
    echo [+] Entorno virtual encontrado.
    call .venv\Scripts\activate.bat
)

echo.
echo [+] Iniciando servidor...
echo.
uvicorn app.main:app --reload

pause