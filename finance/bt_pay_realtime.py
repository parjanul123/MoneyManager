"""
Real-time BT Pay data streaming
Exposes live transaction data via API
"""

import json
from decimal import Decimal
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
import time

from .models import BankTransaction, Transaction
from .bt_pay_service import BTPay


class DecimalEncoder(json.JSONEncoder):
    """JSON encoder for Decimal values"""
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


@login_required
@require_http_methods(["GET"])
def bt_pay_live_transactions(request):
    """
    Real-time BT Pay transactions stream
    Returns: { transactions: [...], timestamp: "...", count: N }
    """
    
    # Get last N minutes
    minutes = int(request.GET.get('minutes', 60))
    limit = int(request.GET.get('limit', 50))
    
    start_time = timezone.now() - timedelta(minutes=minutes)
    
    # Get recent pending transactions
    recent = BankTransaction.objects.filter(
        user=request.user,
        date__gte=start_time
    ).exclude(description__isnull=True).order_by('-date')[:limit]
    
    transactions = []
    for trans in recent:
        is_bt_pay = BTPay.is_bt_pay_transaction(trans.description)
        category = BTPay.guess_category(trans.description) if is_bt_pay else None
        
        transactions.append({
            'id': trans.id,
            'merchant': BTPay.extract_merchant_name(trans.description),
            'amount': float(trans.amount),
            'currency': trans.currency,
            'date': trans.date.isoformat(),
            'category': category,
            'is_bt_pay': is_bt_pay,
            'status': trans.sync_status,
            'description': trans.description,
        })
    
    return JsonResponse({
        'success': True,
        'transactions': transactions,
        'count': len(transactions),
        'timestamp': timezone.now().isoformat(),
    }, encoder=DecimalEncoder)


@login_required
@require_http_methods(["GET"])
def bt_pay_live_stats(request):
    """
    Real-time statistics
    Returns: { stats_30: {...}, stats_today: {...}, stats_this_month: {...} }
    """
    
    today = timezone.now()
    
    # Today
    stats_today = BTPay.get_bt_pay_stats(request.user, days=1)
    
    # This month
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    days_in_month = (today - month_start).days
    stats_month = BTPay.get_bt_pay_stats(request.user, days=max(1, days_in_month + 1))
    
    # Last 30 days
    stats_30 = BTPay.get_bt_pay_stats(request.user, days=30)
    
    return JsonResponse({
        'success': True,
        'stats': {
            'today': {
                'transactions': stats_today['total_transactions'],
                'amount': float(stats_today['total_amount']),
                'categories': len(stats_today['transactions_by_category']),
            },
            'this_month': {
                'transactions': stats_month['total_transactions'],
                'amount': float(stats_month['total_amount']),
                'categories': len(stats_month['transactions_by_category']),
            },
            'last_30_days': {
                'transactions': stats_30['total_transactions'],
                'amount': float(stats_30['total_amount']),
                'top_merchant': list(stats_30['top_merchants'].keys())[0] if stats_30['top_merchants'] else None,
                'top_merchant_spending': float(list(stats_30['top_merchants'].values())[0]['total']) if stats_30['top_merchants'] else 0,
            }
        },
        'timestamp': today.isoformat(),
    }, encoder=DecimalEncoder)


@login_required
@require_http_methods(["GET"])
def bt_pay_live_pending(request):
    """
    Real-time pending transactions count and details
    """
    
    pending = BankTransaction.objects.filter(
        user=request.user,
        sync_status='pending'
    ).exclude(description__isnull=True).order_by('-date')
    
    pending_bt_pay = [
        t for t in pending 
        if BTPay.is_bt_pay_transaction(t.description)
    ]
    
    pending_list = []
    for trans in pending_bt_pay[:20]:  # Top 20
        pending_list.append({
            'id': trans.id,
            'merchant': BTPay.extract_merchant_name(trans.description),
            'amount': float(abs(trans.amount)),
            'currency': trans.currency,
            'date': trans.date.isoformat(),
            'category_guess': BTPay.guess_category(trans.description),
            'description': trans.description,
        })
    
    return JsonResponse({
        'success': True,
        'pending_count': len(pending_bt_pay),
        'pending_transactions': pending_list,
        'total_pending_amount': float(sum(abs(t.amount) for t in pending_bt_pay)),
        'timestamp': timezone.now().isoformat(),
    }, encoder=DecimalEncoder)


@login_required
@require_http_methods(["GET"])
def bt_pay_live_dashboard_data(request):
    """
    Complete real-time dashboard data
    All data needed for live dashboard update
    """
    
    # Stats
    stats_30 = BTPay.get_bt_pay_stats(request.user, days=30)
    stats_today = BTPay.get_bt_pay_stats(request.user, days=1)
    
    # Pending
    pending = BankTransaction.objects.filter(
        user=request.user,
        sync_status='pending'
    ).exclude(description__isnull=True).order_by('-date')
    
    pending_bt_pay = [
        t for t in pending 
        if BTPay.is_bt_pay_transaction(t.description)
    ]
    
    # Recent synced
    recent = BankTransaction.objects.filter(
        user=request.user,
        sync_status='synced',
        date__gte=timezone.now() - timedelta(days=7)
    ).exclude(description__isnull=True).order_by('-date')[:10]
    
    recent_list = []
    for trans in recent:
        recent_list.append({
            'merchant': BTPay.extract_merchant_name(trans.description),
            'amount': float(abs(trans.amount)),
            'date': trans.date.isoformat(),
            'category': BTPay.guess_category(trans.description),
        })
    
    return JsonResponse({
        'success': True,
        'dashboard': {
            'pending_count': len(pending_bt_pay),
            'pending_amount': float(sum(abs(t.amount) for t in pending_bt_pay)),
            'today_transactions': stats_today['total_transactions'],
            'today_amount': float(stats_today['total_amount']),
            'month_transactions': stats_30['total_transactions'],
            'month_amount': float(stats_30['total_amount']),
            'month_merchants': len(stats_30['top_merchants']),
            'top_merchants': [
                {
                    'name': name,
                    'amount': float(data['total']),
                    'count': data['count']
                }
                for name, data in list(stats_30['top_merchants'].items())[:5]
            ],
            'recent_transactions': recent_list,
        },
        'timestamp': timezone.now().isoformat(),
    }, encoder=DecimalEncoder)


def stream_bt_pay_events(request):
    """
    Server-Sent Events (SSE) stream for real-time updates
    Client connects and receives updates every N seconds
    """
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    def event_stream():
        interval = int(request.GET.get('interval', 5))  # seconds
        duration = int(request.GET.get('duration', 300))  # 5 minutes
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                # Get latest data
                pending = BankTransaction.objects.filter(
                    user=request.user,
                    sync_status='pending'
                ).exclude(description__isnull=True).count()
                
                pending_bt_pay = BankTransaction.objects.filter(
                    user=request.user,
                    sync_status='pending'
                ).exclude(description__isnull=True)
                
                pending_bt_pay_count = sum(
                    1 for t in pending_bt_pay 
                    if BTPay.is_bt_pay_transaction(t.description)
                )
                
                # Get stats
                stats = BTPay.get_bt_pay_stats(request.user, days=1)
                
                # Format SSE event
                data = {
                    'pending_bt_pay': pending_bt_pay_count,
                    'today_transactions': stats['total_transactions'],
                    'today_amount': float(stats['total_amount']),
                    'timestamp': timezone.now().isoformat(),
                }
                
                yield f'data: {json.dumps(data)}\n\n'
                
                time.sleep(interval)
                
            except Exception as e:
                yield f'data: {json.dumps({"error": str(e)})}\n\n'
                time.sleep(interval)
    
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


@login_required
@require_http_methods(["GET"])
def bt_pay_hourly_summary(request):
    """
    Hourly summary for last 24 hours
    """
    
    now = timezone.now()
    hours_data = []
    
    for i in range(24, 0, -1):
        hour_start = now - timedelta(hours=i)
        hour_end = hour_start + timedelta(hours=1)
        
        transactions = BankTransaction.objects.filter(
            user=request.user,
            sync_status='synced',
            date__gte=hour_start,
            date__lt=hour_end
        ).exclude(description__isnull=True)
        
        bt_pay_trans = [
            t for t in transactions 
            if BTPay.is_bt_pay_transaction(t.description)
        ]
        
        hours_data.append({
            'hour': hour_start.hour,
            'timestamp': hour_start.isoformat(),
            'count': len(bt_pay_trans),
            'amount': float(sum(abs(t.amount) for t in bt_pay_trans)),
        })
    
    return JsonResponse({
        'success': True,
        'hours': hours_data,
        'total_transactions': sum(h['count'] for h in hours_data),
        'total_amount': sum(h['amount'] for h in hours_data),
    }, encoder=DecimalEncoder)


@login_required
@require_http_methods(["GET"])
def bt_pay_category_realtime(request):
    """
    Real-time category breakdown
    """
    
    stats_24h = BTPay.get_bt_pay_stats(request.user, days=1)
    stats_7d = BTPay.get_bt_pay_stats(request.user, days=7)
    
    categories = {}
    for category, data in stats_7d['transactions_by_category'].items():
        today_data = stats_24h['transactions_by_category'].get(category, {
            'count': 0,
            'total': Decimal('0')
        })
        
        categories[category] = {
            'today': {
                'count': today_data['count'],
                'amount': float(today_data['total']),
            },
            'week': {
                'count': data['count'],
                'amount': float(data['total']),
            }
        }
    
    return JsonResponse({
        'success': True,
        'categories': categories,
        'timestamp': timezone.now().isoformat(),
    }, encoder=DecimalEncoder)
