@echo off
TITLE Generando Replicant.exe...
color 0A

echo ===================================================
echo    CONSTRUCTOR DE REPLICANT PARA WINDOWS
echo ===================================================
echo.

:: 1. Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo Por favor instala Python desde python.org y marca "Add to PATH".
    pause
    exit /b
)

:: 2. Crear entorno virtual (opcional pero recomendado)
if not exist "venv_win" (
    echo [INFO] Creando entorno virtual...
    python -m venv venv_win
)

:: 3. Activar entorno e instalar dependencias
echo [INFO] Instalando dependencias...
call venv_win\Scripts\activate
pip install -r requirements.txt

:: 4. Construir el EXE
echo.
echo [INFO] Generando ejecutable...
python build.py

:: 5. Finalizar
echo.
echo ===================================================
echo    EXITO! El ejecutable esta en la carpeta 'dist'
echo ===================================================
echo.
explorer "dist\Replicant"
pause
