@echo off
echo Demarrage du serveur API Atlas...
echo.
echo Routes disponibles:
echo - GET /atlas.json              : Donnees JSON completes
echo - GET /atlas/{index}.png       : Image atlas par index
echo.
echo Serveur demarre sur http://localhost:8000
echo Appuyez sur Ctrl+C pour arreter
echo.

cd /d "%~dp0"
php -S localhost:8000 api.php
