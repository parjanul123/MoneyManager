"""
Vederile pentru gestionarea conectării și sincronizării cu băncile
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum, Q, Count
from django.utils import timezone
from datetime import timedelta

from .models import BankConnection, BankTransaction, Transaction, Account, Category
from .forms import BankConnectionForm, BankTransactionSyncForm, BankTransactionReviewForm
from .bank_services import (
    BankServiceFactory, 
    sync_all_banks, 
    update_account_balance,
    auto_sync_pending_transactions
)
import logging

logger = logging.getLogger(__name__)


@login_required
def bank_connections_list(request):
    """Afișează lista de conectări la bănci"""
    connections = BankConnection.objects.filter(user=request.user)
    
    context = {
        'connections': connections,
        'page_title': 'Conturile Mele Bancare',
    }
    
    return render(request, 'finance/bank_connections_list.html', context)


@login_required
def bank_connection_create(request):
    """Creează o nouă conectare la bancă"""
    if request.method == 'POST':
        form = BankConnectionForm(request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            connection.user = request.user
            
            try:
                # Testează conexiunea
                service = BankServiceFactory.get_service(connection)
                balance_data = service.get_balance()
                
                if balance_data:
                    connection.save()
                    
                    # Actualizează soldul
                    account, created = Account.objects.get_or_create(
                        user=request.user,
                        name=connection.account_name,
                        defaults={
                            'type': 'checking',
                            'currency': balance_data.get('currency', 'RON'),
                            'balance': balance_data.get('balance', 0),
                        }
                    )
                    
                    if not created:
                        account.balance = balance_data.get('balance', 0)
                        account.currency = balance_data.get('currency', 'RON')
                        account.save()
                    
                    messages.success(
                        request, 
                        f"✓ Conectare la {connection.get_bank_display()} reușită! Sold: {balance_data.get('balance')} {balance_data.get('currency')}"
                    )
                    return redirect('bank_connections_list')
                else:
                    messages.error(request, "✗ Nu s-a putut conecta la bancă. Verifică token-ul.")
            except Exception as e:
                logger.error(f"Error connecting to bank: {str(e)}")
                messages.error(request, f"✗ Eroare de conexiune: {str(e)}")
    else:
        form = BankConnectionForm()
    
    context = {
        'form': form,
        'page_title': 'Conectare la Bancă',
    }
    
    return render(request, 'finance/bank_connection_form.html', context)


@login_required
def bank_connection_delete(request, pk):
    """Șterge o conectare la bancă"""
    connection = get_object_or_404(BankConnection, pk=pk, user=request.user)
    
    if request.method == 'POST':
        bank_name = connection.get_bank_display()
        connection.delete()
        messages.success(request, f"✓ Conectarea la {bank_name} a fost ștearsă.")
        return redirect('bank_connections_list')
    
    context = {
        'connection': connection,
        'page_title': f'Ștergere {connection.get_bank_display()}',
    }
    
    return render(request, 'finance/bank_connection_confirm_delete.html', context)


@login_required
def bank_sync_transactions(request, pk=None):
    """Sincronizează tranzacții din bănci"""
    if pk:
        connection = get_object_or_404(BankConnection, pk=pk, user=request.user)
        connections = [connection]
    else:
        connections = BankConnection.objects.filter(user=request.user, is_active=True)
    
    if request.method == 'POST':
        form = BankTransactionSyncForm(request.POST)
        if form.is_valid():
            days_back = form.cleaned_data['days_back']
            auto_create = form.cleaned_data['auto_create_transactions']
            
            total_synced = 0
            
            for connection in connections:
                try:
                    service = BankServiceFactory.get_service(connection)
                    synced = service.sync_transactions(days_back=days_back)
                    total_synced += synced
                    
                    # Actualizează soldul
                    update_account_balance(connection)
                    
                except Exception as e:
                    logger.error(f"Sync error: {str(e)}")
                    messages.error(request, f"Eroare sincronizare {connection.get_bank_display()}: {str(e)}")
            
            if total_synced > 0:
                messages.success(request, f"✓ Sincronizate {total_synced} tranzacții!")
            else:
                messages.info(request, "Nicio tranzacție nouă.")
            
            if auto_create:
                auto_synced = auto_sync_pending_transactions(request.user)
                if auto_synced > 0:
                    messages.success(request, f"✓ Creată {auto_synced} tranzacție(i) automat!")
            
            if pk:
                return redirect('bank_transaction_pending', pk=pk)
            else:
                return redirect('bank_transactions_pending')
    else:
        form = BankTransactionSyncForm()
    
    context = {
        'form': form,
        'connections': connections,
        'page_title': 'Sincronizare Tranzacții Bancare',
    }
    
    return render(request, 'finance/bank_sync_form.html', context)


@login_required
def bank_transactions_pending(request, pk=None):
    """Afișează tranzacțiile în așteptare pentru revizuire"""
    if pk:
        connection = get_object_or_404(BankConnection, pk=pk, user=request.user)
        transactions = BankTransaction.objects.filter(
            user=request.user,
            bank_connection=connection,
            sync_status='pending'
        )
        title = f"Tranzacții {connection.get_bank_display()}"
    else:
        transactions = BankTransaction.objects.filter(
            user=request.user,
            sync_status='pending'
        )
        title = "Tranzacții în Așteptare"
    
    # Agregare statistici
    stats = transactions.aggregate(
        total_income=Sum('amount', filter=Q(amount__gt=0)),
        total_expense=Sum('amount', filter=Q(amount__lt=0)),
        count=Count('id')
    )
    
    context = {
        'transactions': transactions,
        'stats': stats,
        'page_title': title,
    }
    
    return render(request, 'finance/bank_transactions_pending.html', context)


@login_required
@require_POST
def bank_transaction_accept(request, trans_pk):
    """Acceptă și creează o tranzacție în cont"""
    bank_trans = get_object_or_404(BankTransaction, pk=trans_pk, user=request.user)
    
    category_id = request.POST.get('category_id')
    description = request.POST.get('description', bank_trans.description)
    
    try:
        # Selectează categoria
        category = None
        if category_id:
            category = Category.objects.get(id=category_id)
        
        # Selectează contul pe bază de monedă
        account = Account.objects.filter(
            user=request.user,
            currency=bank_trans.currency
        ).first()
        
        if not account:
            messages.error(request, "Niciun cont cu această monedă. Creaează un cont mai întâi.")
            return redirect('bank_transactions_pending')
        
        # Creează tranzacția
        transaction = Transaction.objects.create(
            user=request.user,
            account=account,
            category=category,
            type='income' if bank_trans.amount > 0 else 'expense',
            amount=abs(bank_trans.amount),
            description=description,
            date=bank_trans.date.date(),
        )
        
        bank_trans.synced_to_transaction = transaction
        bank_trans.sync_status = 'synced'
        bank_trans.save()
        
        messages.success(request, "✓ Tranzacție acceptată și creată.")
        
    except Exception as e:
        logger.error(f"Error accepting transaction: {str(e)}")
        messages.error(request, f"Eroare: {str(e)}")
    
    return redirect('bank_transactions_pending')


@login_required
@require_POST
def bank_transaction_ignore(request, trans_pk):
    """Ignoră o tranzacție din bănci"""
    bank_trans = get_object_or_404(BankTransaction, pk=trans_pk, user=request.user)
    
    bank_trans.sync_status = 'ignored'
    bank_trans.save()
    
    messages.info(request, "Tranzacție ignorată.")
    return redirect('bank_transactions_pending')


@login_required
def bank_transactions_synced(request, pk=None):
    """Afișează tranzacții sincronizate"""
    if pk:
        connection = get_object_or_404(BankConnection, pk=pk, user=request.user)
        transactions = BankTransaction.objects.filter(
            user=request.user,
            bank_connection=connection,
            sync_status='synced'
        )
        title = f"Tranzacții Sincronizate - {connection.get_bank_display()}"
    else:
        transactions = BankTransaction.objects.filter(
            user=request.user,
            sync_status='synced'
        )
        title = "Tranzacții Sincronizate"
    
    stats = transactions.aggregate(
        total_income=Sum('amount', filter=Q(amount__gt=0)),
        total_expense=Sum('amount', filter=Q(amount__lt=0)),
        count=Count('id')
    )
    
    context = {
        'transactions': transactions,
        'stats': stats,
        'page_title': title,
    }
    
    return render(request, 'finance/bank_transactions_synced.html', context)


@login_required
def bank_dashboard(request):
    """Dashboard cu informații din bănci"""
    connections = BankConnection.objects.filter(user=request.user, is_active=True)
    
    # Sincronizări recente
    synced_transactions = BankTransaction.objects.filter(
        user=request.user,
        sync_status='synced'
    ).order_by('-created_at')[:5]
    
    pending_transactions = BankTransaction.objects.filter(
        user=request.user,
        sync_status='pending'
    ).count()
    
    # Statistici pe ultimii 30 zile
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_transactions = BankTransaction.objects.filter(
        user=request.user,
        date__gte=thirty_days_ago,
        sync_status='synced'
    )
    
    stats = recent_transactions.aggregate(
        total_income=Sum('amount', filter=Q(amount__gt=0)),
        total_expense=Sum('amount', filter=Q(amount__lt=0)),
    )
    
    context = {
        'connections': connections,
        'synced_transactions': synced_transactions,
        'pending_count': pending_transactions,
        'stats': stats,
        'page_title': 'Dashboard Bancar',
    }
    
    return render(request, 'finance/bank_dashboard.html', context)
