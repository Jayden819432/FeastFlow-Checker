@echo off
echo =====================================================
echo   FeastFlow Checker - Windows EXE Builder
echo =====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.11+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

echo Python detected!
echo.

echo Installing dependencies...
echo.
python -m pip install --upgrade pip
python -m pip install PyQt6 pyinstaller Pillow

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo =====================================================
echo   Building Windows Executable...
echo =====================================================
echo.

python -m PyInstaller FeastFlow_Checker.spec --clean --noconfirm --log-level=WARN

if errorlevel 1 (
    echo.
    echo =====================================================
    echo ERROR: Build failed!
    echo =====================================================
    pause
    exit /b 1
)

echo.
echo =====================================================
echo SUCCESS! Build completed!
echo =====================================================
echo.
echo Your executable is located at:
echo   dist\FeastFlow_Checker.exe
echo.
echo You can now run this .exe on any Windows 10-11 computer!
echo.
echo =====================================================
pause
