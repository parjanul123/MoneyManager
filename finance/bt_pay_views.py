"""
BT Pay Dashboard Views
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from datetime import timedelta
from django.utils import timezone

from .models import BankTransaction, Transaction
from .bt_pay_service import BTPay


@login_required
def bt_pay_websocket_dashboard(request):
    """BT Pay WebSocket Dashboard - Real-time push via WebSocket"""
    return render(request, 'finance/bt_pay_websocket.html')


@login_required
def bt_pay_live_dashboard(request):
    """BT Pay Live Dashboard - Real-time updates via JavaScript"""
    return render(request, 'finance/bt_pay_live_dashboard.html')


@login_required
def bt_pay_dashboard(request):
    """BT Pay Dashboard - Overview și statistici"""
    
    # Tranzacții pending
    pending_bt_pay = BankTransaction.objects.filter(
        user=request.user,
        sync_status='pending'
    ).exclude(description__isnull=True)
    
    pending_bt_pay = [
        t for t in pending_bt_pay 
        if BTPay.is_bt_pay_transaction(t.description)
    ]
    
    # Stats ultimele 30 zile
    stats_30 = BTPay.get_bt_pay_stats(request.user, days=30)
    
    # Stats ultimele 90 zile
    stats_90 = BTPay.get_bt_pay_stats(request.user, days=90)
    
    # Trend lunar
    today = timezone.now()
    months = []
    for i in range(5):
        month_date = today - timedelta(days=30*i)
        start = month_date.replace(day=1)
        end = (start + timedelta(days=32)).replace(day=1)
        
        bt_pay_trans = BankTransaction.objects.filter(
            user=request.user,
            sync_status='synced',
            date__gte=start,
            date__lt=end
        ).exclude(description__isnull=True)
        
        bt_pay_trans = [
            t for t in bt_pay_trans 
            if BTPay.is_bt_pay_transaction(t.description)
        ]
        
        total = sum(abs(t.amount) for t in bt_pay_trans)
        
        months.append({
            'month': month_date.strftime('%B'),
            'total': float(total),
            'count': len(bt_pay_trans)
        })
    
    context = {
        'pending_bt_pay': pending_bt_pay,
        'pending_count': len(pending_bt_pay),
        'stats_30': stats_30,
        'stats_90': stats_90,
        'months': months,
        'total_merchants': len(stats_30['top_merchants']),
    }
    
    return render(request, 'finance/bt_pay_dashboard.html', context)


@login_required
def bt_pay_transactions(request):
    """Lista tuturor tranzacțiilor BT Pay"""
    
    # Parametri filtrare
    days = int(request.GET.get('days', 30))
    category = request.GET.get('category', '')
    merchant = request.GET.get('merchant', '')
    
    start_date = timezone.now() - timedelta(days=days)
    
    # Bază query
    bt_pay_trans = BankTransaction.objects.filter(
        user=request.user,
        sync_status='synced',
        date__gte=start_date
    ).exclude(description__isnull=True).order_by('-date')
    
    # Filtrează după BT Pay
    bt_pay_list = [
        t for t in bt_pay_trans 
        if BTPay.is_bt_pay_transaction(t.description)
    ]
    
    # Filtrare după categorie
    if category:
        bt_pay_list = [
            t for t in bt_pay_list 
            if BTPay.guess_category(t.description) == category
        ]
    
    # Filtrare după comerciant
    if merchant:
        merchant_lower = merchant.lower()
        bt_pay_list = [
            t for t in bt_pay_list 
            if merchant_lower in BTPay.extract_merchant_name(t.description).lower()
        ]
    
    context = {
        'transactions': bt_pay_list,
        'days': days,
        'category': category,
        'merchant': merchant,
        'categories': list(BTPay.MERCHANT_CATEGORIES.keys()),
    }
    
    return render(request, 'finance/bt_pay_transactions.html', context)


@login_required
@require_http_methods(["POST"])
def bt_pay_auto_categorize(request):
    """Auto-categorizează tranzacții BT Pay"""
    
    categorized = BTPay.auto_categorize_all_bt_pay(request.user)
    
    return JsonResponse({
        'success': True,
        'categorized': categorized,
        'message': f'Successfully auto-categorized {categorized} BT Pay transactions'
    })


@login_required
def bt_pay_merchant_detail(request, merchant_name):
    """Detalii despre un anumit comerciant"""
    
    # Toate tranzacțiile cu acest comerciant
    all_transactions = BankTransaction.objects.filter(
        user=request.user,
        sync_status='synced'
    ).exclude(description__isnull=True).order_by('-date')
    
    merchant_trans = [
        t for t in all_transactions
        if BTPay.is_bt_pay_transaction(t.description)
        and merchant_name.lower() in BTPay.extract_merchant_name(t.description).lower()
    ]
    
    # Statistici
    stats = {
        'merchant': merchant_name,
        'total_transactions': len(merchant_trans),
        'total_spent': sum(abs(t.amount) for t in merchant_trans),
        'average_transaction': sum(abs(t.amount) for t in merchant_trans) / len(merchant_trans) if merchant_trans else 0,
        'currency': merchant_trans[0].currency if merchant_trans else 'RON',
        'first_transaction': merchant_trans[-1].date if merchant_trans else None,
        'last_transaction': merchant_trans[0].date if merchant_trans else None,
        'transactions': merchant_trans[:50]  # Ultimele 50
    }
    
    return render(request, 'finance/bt_pay_merchant_detail.html', {'stats': stats})


@login_required
def bt_pay_category_analysis(request):
    """Analiză detaliată pe categorii"""
    
    days = int(request.GET.get('days', 30))
    
    start_date = timezone.now() - timedelta(days=days)
    
    all_transactions = BankTransaction.objects.filter(
        user=request.user,
        sync_status='synced',
        date__gte=start_date
    ).exclude(description__isnull=True)
    
    bt_pay_trans = [
        t for t in all_transactions 
        if BTPay.is_bt_pay_transaction(t.description)
    ]
    
    # Analiză pe categorii
    categories_analysis = {}
    for trans in bt_pay_trans:
        category = BTPay.guess_category(trans.description) or 'other'
        
        if category not in categories_analysis:
            categories_analysis[category] = {
                'total': 0,
                'count': 0,
                'average': 0,
                'max': 0,
                'min': float('inf'),
                'merchants': {}
            }
        
        amount = abs(trans.amount)
        categories_analysis[category]['total'] += amount
        categories_analysis[category]['count'] += 1
        categories_analysis[category]['max'] = max(categories_analysis[category]['max'], amount)
        categories_analysis[category]['min'] = min(categories_analysis[category]['min'], amount)
        
        # Track merchants
        merchant = BTPay.extract_merchant_name(trans.description) or 'Unknown'
        if merchant not in categories_analysis[category]['merchants']:
            categories_analysis[category]['merchants'][merchant] = 0
        categories_analysis[category]['merchants'][merchant] += 1
    
    # Calculează medii
    for cat in categories_analysis:
        if categories_analysis[cat]['count'] > 0:
            categories_analysis[cat]['average'] = categories_analysis[cat]['total'] / categories_analysis[cat]['count']
        if categories_analysis[cat]['min'] == float('inf'):
            categories_analysis[cat]['min'] = 0
    
    # Sortează
    sorted_categories = sorted(
        categories_analysis.items(),
        key=lambda x: x[1]['total'],
        reverse=True
    )
    
    context = {
        'categories': dict(sorted_categories),
        'days': days,
        'currency': 'RON',
    }
    
    return render(request, 'finance/bt_pay_category_analysis.html', context)
