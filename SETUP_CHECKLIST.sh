#!/bin/bash
# Bank Integration Setup Checklist
# Rulează: bash SETUP_CHECKLIST.sh

echo "=================================================="
echo "🏦 Money Manager - Bank Integration Setup"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_mark="${GREEN}✓${NC}"
cross="${RED}✗${NC}"

# 1. Check Python
echo -n "1. Verificare Python... "
if command -v python &> /dev/null; then
    echo -e "$check_mark Python instalat"
else
    echo -e "$cross Python nu este instalat"
fi

# 2. Check Django
echo -n "2. Verificare Django... "
python -c "import django" 2>/dev/null && echo -e "$check_mark Django instalat" || echo -e "$cross Django nu este instalat"

# 3. Check requirements
echo -n "3. Verificare requirements.txt... "
if [ -f "requirements.txt" ]; then
    echo -e "$check_mark requirements.txt găsit"
    
    echo -n "   - requests... "
    grep -q "requests" requirements.txt && echo -e "$check_mark" || echo -e "$cross"
    
    echo -n "   - cryptography... "
    grep -q "cryptography" requirements.txt && echo -e "$check_mark" || echo -e "$cross"
else
    echo -e "$cross requirements.txt nu găsit"
fi

# 4. Check models
echo -n "4. Verificare modele... "
if grep -q "class BankConnection" finance/models.py && grep -q "class BankTransaction" finance/models.py; then
    echo -e "$check_mark Modele definite"
else
    echo -e "$cross Modele nu sunt complete"
fi

# 5. Check services
echo -n "5. Verificare servicii API... "
if [ -f "finance/bank_services.py" ]; then
    echo -e "$check_mark bank_services.py găsit"
    
    echo -n "   - RevolutBankService... "
    grep -q "class RevolutBankService" finance/bank_services.py && echo -e "$check_mark" || echo -e "$cross"
    
    echo -n "   - BTBankService... "
    grep -q "class BTBankService" finance/bank_services.py && echo -e "$check_mark" || echo -e "$cross"
else
    echo -e "$cross bank_services.py nu găsit"
fi

# 6. Check views
echo -n "6. Verificare vederile web... "
if [ -f "finance/bank_views.py" ]; then
    echo -e "$check_mark bank_views.py găsit"
else
    echo -e "$cross bank_views.py nu găsit"
fi

# 7. Check templates
echo -n "7. Verificare template-uri... "
if [ -d "finance/templates/finance" ]; then
    count=$(ls finance/templates/finance/bank_*.html 2>/dev/null | wc -l)
    echo -e "$check_mark $count template-uri găsite"
else
    echo -e "$cross Folder de template-uri nu găsit"
fi

# 8. Check URLs
echo -n "8. Verificare URL routes... "
if grep -q "bank_views" finance/urls.py; then
    echo -e "$check_mark URL-urile pentru bănci sunt configurate"
else
    echo -e "$cross URL-urile nu sunt configurate"
fi

# 9. Check admin
echo -n "9. Verificare admin interface... "
if grep -q "BankConnectionAdmin" finance/admin.py && grep -q "BankTransactionAdmin" finance/admin.py; then
    echo -e "$check_mark Admin classes definite"
else
    echo -e "$cross Admin classes nu sunt complete"
fi

# 10. Check migrations
echo -n "10. Verificare migration file... "
if [ -f "finance/migrations/0003_bank_integration.py" ]; then
    echo -e "$check_mark Migration file găsit"
else
    echo -e "$cross Migration file nu găsit"
fi

# 11. Check forms
echo -n "11. Verificare formulare... "
if grep -q "class BankConnectionForm" finance/forms.py; then
    echo -e "$check_mark Formulare definite"
else
    echo -e "$cross Formulare nu sunt complete"
fi

# 12. Check documentation
echo -n "12. Verificare documentație... "
docs_found=0
[ -f "BANK_INTEGRATION_GUIDE.md" ] && ((docs_found++))
[ -f "BANK_INTEGRATION_QUICKSTART.md" ] && ((docs_found++))
[ -f "BANK_INTEGRATION_SUMMARY.md" ] && ((docs_found++))
echo -e "$check_mark $docs_found fișiere de documentație"

# 13. Check test file
echo -n "13. Verificare teste... "
if [ -f "finance/tests_bank_integration.py" ]; then
    echo -e "$check_mark Test file găsit"
else
    echo -e "$cross Test file nu găsit"
fi

# 14. Check management command
echo -n "14. Verificare management command... "
if [ -f "finance/management/commands/sync_bank_transactions.py" ]; then
    echo -e "$check_mark Management command găsit"
else
    echo -e "$cross Management command nu găsit"
fi

# 15. Check setup script
echo -n "15. Verificare setup script... "
if [ -f "setup_bank_integration.py" ]; then
    echo -e "$check_mark Setup script găsit"
else
    echo -e "$cross Setup script nu găsit"
fi

echo ""
echo "=================================================="
echo "URMATORU PASI:"
echo "=================================================="
echo ""
echo "1. Instalează pachete:"
echo "   ${YELLOW}pip install -r requirements.txt${NC}"
echo ""
echo "2. Aplică migrații:"
echo "   ${YELLOW}python manage.py makemigrations finance${NC}"
echo "   ${YELLOW}python manage.py migrate${NC}"
echo ""
echo "3. Setup categorii:"
echo "   ${YELLOW}python setup_bank_integration.py${NC}"
echo ""
echo "4. Testare:"
echo "   ${YELLOW}python manage.py test finance.tests_bank_integration${NC}"
echo ""
echo "5. Pornire server:"
echo "   ${YELLOW}python manage.py runserver${NC}"
echo ""
echo "6. Acceseaza: http://localhost:8000/finance/banks/"
echo ""
echo "=================================================="
echo "DOCUMENTAȚIE:"
echo "=================================================="
echo ""
echo "📖 Ghid Complet: BANK_INTEGRATION_GUIDE.md"
echo "⚡ Quick Start: BANK_INTEGRATION_QUICKSTART.md"
echo "📋 Sumar: BANK_INTEGRATION_SUMMARY.md"
echo ""
echo "=================================================="
