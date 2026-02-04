"""
Django Channels WebSocket consumers for BT Pay real-time updates
"""

import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from datetime import timedelta

from .models import BankTransaction
from .bt_pay_service import BTPay


class BTPayliveConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time BT Pay updates"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        if not self.scope['user'].is_authenticated:
            await self.close()
            return
        
        self.user_id = self.scope['user'].id
        self.room_group_name = f'btpay_{self.user_id}'
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        # Send initial data
        await self.send_initial_data()
        
        # Start periodic updates
        asyncio.create_task(self.periodic_updates())
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data):
        """Handle incoming messages"""
        data = json.loads(text_data)
        command = data.get('command')
        
        if command == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong', 'timestamp': timezone.now().isoformat()}))
        
        elif command == 'request_data':
            await self.send_dashboard_data()
        
        elif command == 'request_pending':
            await self.send_pending_data()
        
        elif command == 'request_hourly':
            await self.send_hourly_data()
        
        elif command == 'request_categories':
            await self.send_category_data()
        
        elif command == 'auto_categorize':
            await self.auto_categorize()
    
    async def send_initial_data(self):
        """Send all data on connection"""
        await self.send_dashboard_data()
        await self.send_pending_data()
        await self.send_hourly_data()
        await self.send_category_data()
    
    async def send_dashboard_data(self):
        """Send dashboard data"""
        data = await self.get_dashboard_data()
        await self.send(text_data=json.dumps({
            'type': 'dashboard_update',
            'data': data,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def send_pending_data(self):
        """Send pending transactions"""
        data = await self.get_pending_data()
        await self.send(text_data=json.dumps({
            'type': 'pending_update',
            'data': data,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def send_hourly_data(self):
        """Send hourly breakdown"""
        data = await self.get_hourly_data()
        await self.send(text_data=json.dumps({
            'type': 'hourly_update',
            'data': data,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def send_category_data(self):
        """Send category breakdown"""
        data = await self.get_category_data()
        await self.send(text_data=json.dumps({
            'type': 'category_update',
            'data': data,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def auto_categorize(self):
        """Auto-categorize pending transactions"""
        result = await self.run_auto_categorize()
        
        await self.send(text_data=json.dumps({
            'type': 'auto_categorize_result',
            'categorized': result,
            'timestamp': timezone.now().isoformat()
        }))
        
        # Send updated data
        await self.send_dashboard_data()
        await self.send_pending_data()
        await self.send_category_data()
    
    async def periodic_updates(self):
        """Send periodic updates"""
        while True:
            try:
                await asyncio.sleep(5)  # Update every 5 seconds
                
                # Check for new transactions
                pending_count = await self.get_pending_count()
                
                await self.send(text_data=json.dumps({
                    'type': 'periodic_update',
                    'pending_count': pending_count,
                    'timestamp': timezone.now().isoformat()
                }))
                
            except Exception as e:
                print(f"Error in periodic updates: {e}")
                break
    
    # Database operations (must be async)
    @database_sync_to_async
    def get_dashboard_data(self):
        """Get dashboard data from database"""
        from django.contrib.auth.models import User
        user = User.objects.get(id=self.user_id)
        
        stats_30 = BTPay.get_bt_pay_stats(user, days=30)
        stats_today = BTPay.get_bt_pay_stats(user, days=1)
        
        # Pending
        pending = BankTransaction.objects.filter(
            user=user,
            sync_status='pending'
        ).exclude(description__isnull=True).order_by('-date')
        
        pending_bt_pay = [
            t for t in pending 
            if BTPay.is_bt_pay_transaction(t.description)
        ]
        
        # Recent
        recent = BankTransaction.objects.filter(
            user=user,
            sync_status='synced',
            date__gte=timezone.now() - timedelta(days=7)
        ).exclude(description__isnull=True).order_by('-date')[:10]
        
        recent_list = [
            {
                'merchant': BTPay.extract_merchant_name(t.description),
                'amount': float(abs(t.amount)),
                'date': t.date.isoformat(),
                'category': BTPay.guess_category(t.description),
            }
            for t in recent
        ]
        
        return {
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
        }
    
    @database_sync_to_async
    def get_pending_data(self):
        """Get pending transactions"""
        from django.contrib.auth.models import User
        user = User.objects.get(id=self.user_id)
        
        pending = BankTransaction.objects.filter(
            user=user,
            sync_status='pending'
        ).exclude(description__isnull=True).order_by('-date')
        
        pending_bt_pay = [
            t for t in pending 
            if BTPay.is_bt_pay_transaction(t.description)
        ]
        
        return [
            {
                'id': t.id,
                'merchant': BTPay.extract_merchant_name(t.description),
                'amount': float(abs(t.amount)),
                'currency': t.currency,
                'date': t.date.isoformat(),
                'category_guess': BTPay.guess_category(t.description),
                'description': t.description,
            }
            for t in pending_bt_pay[:20]
        ]
    
    @database_sync_to_async
    def get_hourly_data(self):
        """Get hourly breakdown"""
        from django.contrib.auth.models import User
        user = User.objects.get(id=self.user_id)
        
        now = timezone.now()
        hours_data = []
        
        for i in range(24, 0, -1):
            hour_start = now - timedelta(hours=i)
            hour_end = hour_start + timedelta(hours=1)
            
            transactions = BankTransaction.objects.filter(
                user=user,
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
        
        return hours_data
    
    @database_sync_to_async
    def get_category_data(self):
        """Get category breakdown"""
        from django.contrib.auth.models import User
        user = User.objects.get(id=self.user_id)
        
        stats_24h = BTPay.get_bt_pay_stats(user, days=1)
        stats_7d = BTPay.get_bt_pay_stats(user, days=7)
        
        categories = {}
        for category, data in stats_7d['transactions_by_category'].items():
            today_data = stats_24h['transactions_by_category'].get(category, {
                'count': 0,
                'total': 0
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
        
        return categories
    
    @database_sync_to_async
    def get_pending_count(self):
        """Get pending transaction count"""
        from django.contrib.auth.models import User
        user = User.objects.get(id=self.user_id)
        
        pending = BankTransaction.objects.filter(
            user=user,
            sync_status='pending'
        ).exclude(description__isnull=True)
        
        return sum(1 for t in pending if BTPay.is_bt_pay_transaction(t.description))
    
    @database_sync_to_async
    def run_auto_categorize(self):
        """Run auto-categorization"""
        from django.contrib.auth.models import User
        user = User.objects.get(id=self.user_id)
        return BTPay.auto_categorize_all_bt_pay(user)


class BTPayNotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for notifications (new transactions, alerts)"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        if not self.scope['user'].is_authenticated:
            await self.close()
            return
        
        self.user_id = self.scope['user'].id
        self.room_group_name = f'btpay_notify_{self.user_id}'
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': 'Connected to notifications',
            'level': 'info'
        }))
    
    async def disconnect(self, close_code):
        """Handle disconnection"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data):
        """Handle incoming messages"""
        data = json.loads(text_data)
        # Currently just for receiving, not sending from client
    
    async def notification_message(self, event):
        """Send notification message"""
        await self.send(text_data=json.dumps(event['data']))
