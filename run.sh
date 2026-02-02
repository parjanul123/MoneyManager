#!/bin/bash
# Script pentru pornirea aplicației Money Manager pe Linux/Mac

echo "========================================"
echo "  Money Manager - Django Application"
echo "========================================"
echo ""

# Activează virtual environment
echo "Activez mediul virtual..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "EROARE: Nu pot activa mediul virtual!"
    exit 1
fi

echo ""
echo "Pornesc serverul Django..."
echo "Aplicația va fi disponibilă la: http://localhost:9512"
echo ""
echo "Pentru admin, mergi la: http://localhost:9512/admin"
echo ""
echo "Apasă CTRL+C pentru a opri serverul"
echo ""

python manage.py runserver 127.0.0.1:9512
