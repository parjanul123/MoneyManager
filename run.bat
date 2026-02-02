@echo off
REM Script pentru pornirea aplicației Money Manager pe Windows

echo.
echo ========================================
echo   Money Manager - Django Application
echo ========================================
echo.

REM Activează virtual environment
echo Activez mediul virtual...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo EROARE: Nu pot activa mediul virtual!
    pause
    exit /b 1
)

echo.
echo Pornesc serverul Django...
echo Aplicația va fi disponibilă la: http://localhost:9512
echo.
echo Pentru admin, mergi la: http://localhost:9512/admin
echo.
echo Apasă CTRL+C pentru a opri serverul
echo.

py manage.py runserver 127.0.0.1:9512

pause
