#!/bin/bash

echo "Démarrage du serveur API Atlas..."
echo ""
echo "Routes disponibles:"
echo "- GET /atlas.json               : Données JSON complètes"
echo "- GET /atlas/{index}.png        : Image atlas par index"
echo ""
echo "Serveur démarré sur http://localhost:8000"
echo "Appuyez sur Ctrl+C pour arrêter"
echo ""

# Change vers le répertoire du script
cd "$(dirname "$0")"

# Démarre le serveur PHP
php -S localhost:8000 api.php