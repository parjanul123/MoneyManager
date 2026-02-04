# Bank Integration Setup Checklist for Windows
# Run: powershell -ExecutionPolicy Bypass -File SETUP_CHECKLIST.ps1

Write-Host "=================================================="
Write-Host "Bank Integration Setup - Money Manager" -ForegroundColor Cyan
Write-Host "=================================================="
Write-Host ""

$checks = @()

# 1. Python
Write-Host -NoNewline "1. Verificare Python... "
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK - $pythonVersion" -ForegroundColor Green
    $checks += @{ name = "Python"; status = "OK" }
} catch {
    Write-Host "FAILED - Python nu este instalat" -ForegroundColor Red
    $checks += @{ name = "Python"; status = "FAILED" }
}

# 2. Django
Write-Host -NoNewline "2. Verificare Django... "
try {
    python -c "import django; print(django.__version__)" | Out-Null
    Write-Host "OK" -ForegroundColor Green
    $checks += @{ name = "Django"; status = "OK" }
} catch {
    Write-Host "FAILED - Django nu este instalat" -ForegroundColor Red
    $checks += @{ name = "Django"; status = "FAILED" }
}

# 3. Requirements
Write-Host -NoNewline "3. Verificare requirements.txt... "
if (Test-Path "requirements.txt") {
    $content = Get-Content "requirements.txt"
    Write-Host "OK" -ForegroundColor Green
    
    if ($content | Select-String "requests") {
        Write-Host "   - requests... OK" -ForegroundColor Green
    } else {
        Write-Host "   - requests... MISSING" -ForegroundColor Yellow
    }
    
    if ($content | Select-String "cryptography") {
        Write-Host "   - cryptography... OK" -ForegroundColor Green
    } else {
        Write-Host "   - cryptography... MISSING" -ForegroundColor Yellow
    }
    $checks += @{ name = "requirements.txt"; status = "OK" }
} else {
    Write-Host "FAILED" -ForegroundColor Red
    $checks += @{ name = "requirements.txt"; status = "FAILED" }
}

# 4. Models
Write-Host -NoNewline "4. Verificare modele... "
$modelsFile = Get-Content "finance\models.py" -ErrorAction SilentlyContinue
if ($modelsFile -match "class BankConnection" -and $modelsFile -match "class BankTransaction") {
    Write-Host "OK" -ForegroundColor Green
    $checks += @{ name = "Modele"; status = "OK" }
} else {
    Write-Host "INCOMPLETE" -ForegroundColor Yellow
    $checks += @{ name = "Modele"; status = "INCOMPLETE" }
}

# 5. Services
Write-Host -NoNewline "5. Verificare bank_services.py... "
if (Test-Path "finance\bank_services.py") {
    Write-Host "OK" -ForegroundColor Green
    $checks += @{ name = "bank_services.py"; status = "OK" }
} else {
    Write-Host "NOT FOUND" -ForegroundColor Red
    $checks += @{ name = "bank_services.py"; status = "NOT FOUND" }
}

# 6. Views
Write-Host -NoNewline "6. Verificare bank_views.py... "
if (Test-Path "finance\bank_views.py") {
    Write-Host "OK" -ForegroundColor Green
    $checks += @{ name = "bank_views.py"; status = "OK" }
} else {
    Write-Host "NOT FOUND" -ForegroundColor Red
    $checks += @{ name = "bank_views.py"; status = "NOT FOUND" }
}

# 7. Templates
Write-Host -NoNewline "7. Verificare template-uri... "
if (Test-Path "finance\templates\finance") {
    $bankTemplates = @(Get-ChildItem "finance\templates\finance\bank_*.html" -ErrorAction SilentlyContinue).Count
    Write-Host "OK - $bankTemplates template-uri" -ForegroundColor Green
    $checks += @{ name = "Template-uri"; status = "OK" }
} else {
    Write-Host "FOLDER NOT FOUND" -ForegroundColor Red
    $checks += @{ name = "Template-uri"; status = "NOT FOUND" }
}

# 8. URLs
Write-Host -NoNewline "8. Verificare URL routes... "
$urlsFile = Get-Content "finance\urls.py" -ErrorAction SilentlyContinue
if ($urlsFile -match "bank_views") {
    Write-Host "OK" -ForegroundColor Green
    $checks += @{ name = "URLs"; status = "OK" }
} else {
    Write-Host "NOT CONFIGURED" -ForegroundColor Yellow
    $checks += @{ name = "URLs"; status = "NOT CONFIGURED" }
}

# 9. Admin
Write-Host -NoNewline "9. Verificare admin.py... "
$adminFile = Get-Content "finance\admin.py" -ErrorAction SilentlyContinue
if ($adminFile -match "BankConnectionAdmin" -and $adminFile -match "BankTransactionAdmin") {
    Write-Host "OK" -ForegroundColor Green
    $checks += @{ name = "Admin"; status = "OK" }
} else {
    Write-Host "INCOMPLETE" -ForegroundColor Yellow
    $checks += @{ name = "Admin"; status = "INCOMPLETE" }
}

# 10. Migrations
Write-Host -NoNewline "10. Verificare migration file... "
if (Test-Path "finance\migrations\0003_bank_integration.py") {
    Write-Host "OK" -ForegroundColor Green
    $checks += @{ name = "Migrations"; status = "OK" }
} else {
    Write-Host "NOT FOUND" -ForegroundColor Red
    $checks += @{ name = "Migrations"; status = "NOT FOUND" }
}

Write-Host ""
Write-Host "=================================================="
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host "=================================================="
Write-Host ""
foreach ($check in $checks) {
    if ($check.status -eq "OK") {
        Write-Host "  $($check.name): " -NoNewline
        Write-Host "$($check.status)" -ForegroundColor Green
    } elseif ($check.status -eq "INCOMPLETE") {
        Write-Host "  $($check.name): " -NoNewline
        Write-Host "$($check.status)" -ForegroundColor Yellow
    } else {
        Write-Host "  $($check.name): " -NoNewline
        Write-Host "$($check.status)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=================================================="
Write-Host "NEXT STEPS" -ForegroundColor Cyan
Write-Host "=================================================="
Write-Host ""
Write-Host "1. Install packages:" -ForegroundColor Yellow
Write-Host "   pip install -r requirements.txt"
Write-Host ""
Write-Host "2. Create migrations:" -ForegroundColor Yellow
Write-Host "   python manage.py makemigrations finance"
Write-Host ""
Write-Host "3. Apply migrations:" -ForegroundColor Yellow
Write-Host "   python manage.py migrate"
Write-Host ""
Write-Host "4. Setup categories:" -ForegroundColor Yellow
Write-Host "   python setup_bank_integration.py"
Write-Host ""
Write-Host "5. Run tests:" -ForegroundColor Yellow
Write-Host "   python manage.py test finance.tests_bank_integration"
Write-Host ""
Write-Host "6. Start server:" -ForegroundColor Yellow
Write-Host "   python manage.py runserver"
Write-Host ""
Write-Host "7. Visit: http://localhost:8000/finance/banks/"
Write-Host ""
Write-Host "=================================================="
Write-Host "DOCUMENTATION" -ForegroundColor Cyan
Write-Host "=================================================="
Write-Host ""
Write-Host "  BANK_INTEGRATION_GUIDE.md - Full guide"
Write-Host "  BANK_INTEGRATION_QUICKSTART.md - Quick start"
Write-Host "  BANK_INTEGRATION_SUMMARY.md - Implementation summary"
Write-Host ""
