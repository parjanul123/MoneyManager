# 📡 BT Pay Real-Time API

## Overview

Acces la date **live** și **în timp real** pentru BT Pay tranzacții. API JSON cu polling automat.

## API Endpoints

### 1. Live Transactions
**Endpoint:** `GET /finance/api/bt-pay/transactions/`

Returnează tranzacțiile recente:

```bash
curl http://localhost:8000/finance/api/bt-pay/transactions/?minutes=60&limit=50
```

**Parameters:**
- `minutes`: Minutes to look back (default: 60)
- `limit`: Max transactions to return (default: 50)

**Response:**
```json
{
  "success": true,
  "transactions": [
    {
      "id": 123,
      "merchant": "Carrefour",
      "amount": -45.50,
      "currency": "RON",
      "date": "2026-02-04T14:30:00Z",
      "category": "shopping",
      "is_bt_pay": true,
      "status": "pending",
      "description": "BT Pay - Carrefour #4521"
    }
  ],
  "count": 15,
  "timestamp": "2026-02-04T14:35:00Z"
}
```

---

### 2. Live Statistics
**Endpoint:** `GET /finance/api/bt-pay/stats/`

Statistici în timp real:

```bash
curl http://localhost:8000/finance/api/bt-pay/stats/
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "today": {
      "transactions": 5,
      "amount": 150.75,
      "categories": 3
    },
    "this_month": {
      "transactions": 87,
      "amount": 3250.50,
      "categories": 8
    },
    "last_30_days": {
      "transactions": 92,
      "amount": 3500.00,
      "top_merchant": "Carrefour",
      "top_merchant_spending": 450.00
    }
  },
  "timestamp": "2026-02-04T14:35:00Z"
}
```

---

### 3. Pending Transactions
**Endpoint:** `GET /finance/api/bt-pay/pending/`

Tranzacții așteptând review:

```bash
curl http://localhost:8000/finance/api/bt-pay/pending/
```

**Response:**
```json
{
  "success": true,
  "pending_count": 12,
  "pending_transactions": [
    {
      "id": 456,
      "merchant": "McDonald's",
      "amount": 25.50,
      "currency": "RON",
      "date": "2026-02-04T12:00:00Z",
      "category_guess": "food",
      "description": "BT Pay - McDonald's #1234"
    }
  ],
  "total_pending_amount": 450.75,
  "timestamp": "2026-02-04T14:35:00Z"
}
```

---

### 4. Dashboard Data (All-in-One)
**Endpoint:** `GET /finance/api/bt-pay/dashboard/`

Toate datele pentru dashboard într-o singură request:

```bash
curl http://localhost:8000/finance/api/bt-pay/dashboard/
```

**Response:**
```json
{
  "success": true,
  "dashboard": {
    "pending_count": 12,
    "pending_amount": 450.75,
    "today_transactions": 5,
    "today_amount": 150.75,
    "month_transactions": 87,
    "month_amount": 3250.50,
    "month_merchants": 8,
    "top_merchants": [
      {
        "name": "Carrefour",
        "amount": 450.00,
        "count": 10
      },
      {
        "name": "Emag",
        "amount": 350.00,
        "count": 5
      }
    ],
    "recent_transactions": [
      {
        "merchant": "Starbucks",
        "amount": 25.00,
        "date": "2026-02-04T14:30:00Z",
        "category": "food"
      }
    ]
  },
  "timestamp": "2026-02-04T14:35:00Z"
}
```

---

### 5. Server-Sent Events (SSE) Stream
**Endpoint:** `GET /finance/api/bt-pay/stream/`

Real-time event stream using Server-Sent Events:

```bash
curl http://localhost:8000/finance/api/bt-pay/stream/?interval=5&duration=300
```

**Parameters:**
- `interval`: Update interval in seconds (default: 5)
- `duration`: Stream duration in seconds (default: 300 = 5 minutes)

**Usage in JavaScript:**
```javascript
const eventSource = new EventSource('/finance/api/bt-pay/stream/?interval=5');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Pending BT Pay:', data.pending_bt_pay);
    console.log('Today transactions:', data.today_transactions);
    console.log('Today amount:', data.today_amount);
};

eventSource.onerror = function() {
    console.error('Connection lost');
    eventSource.close();
};
```

---

### 6. Hourly Summary
**Endpoint:** `GET /finance/api/bt-pay/hourly/`

Breakdown pe ore pentru ultimele 24 ore:

```bash
curl http://localhost:8000/finance/api/bt-pay/hourly/
```

**Response:**
```json
{
  "success": true,
  "hours": [
    {
      "hour": 0,
      "timestamp": "2026-02-03T00:00:00Z",
      "count": 2,
      "amount": 50.00
    },
    {
      "hour": 1,
      "timestamp": "2026-02-03T01:00:00Z",
      "count": 0,
      "amount": 0.00
    },
    {
      "hour": 14,
      "timestamp": "2026-02-04T14:00:00Z",
      "count": 5,
      "amount": 150.75
    }
  ],
  "total_transactions": 87,
  "total_amount": 3250.50
}
```

---

### 7. Categories Real-Time
**Endpoint:** `GET /finance/api/bt-pay/categories/`

Breakdown pe categorii pentru astazi și această săptămână:

```bash
curl http://localhost:8000/finance/api/bt-pay/categories/
```

**Response:**
```json
{
  "success": true,
  "categories": {
    "food": {
      "today": {
        "count": 2,
        "amount": 75.00
      },
      "week": {
        "count": 15,
        "amount": 450.00
      }
    },
    "shopping": {
      "today": {
        "count": 1,
        "amount": 250.00
      },
      "week": {
        "count": 8,
        "amount": 1200.00
      }
    }
  },
  "timestamp": "2026-02-04T14:35:00Z"
}
```

---

## Live Dashboard

**URL:** `http://localhost:8000/finance/bt-pay/`

Features:
- ✅ Real-time metrics (update every 5 seconds)
- ✅ Live pending transactions
- ✅ Recent synced transactions
- ✅ Top merchants with progress bars
- ✅ 24-hour breakdown chart
- ✅ Category spending breakdown
- ✅ Connection status indicator
- ✅ Pause/Resume functionality
- ✅ Manual refresh button

---

## Integration Examples

### 1. Custom Polling in JavaScript

```javascript
async function startPolling(interval = 5000) {
    while (true) {
        const response = await fetch('/finance/api/bt-pay/dashboard/');
        const data = await response.json();
        
        console.log('Pending:', data.dashboard.pending_count);
        console.log('Today:', data.dashboard.today_amount);
        
        // Update UI...
        updateMetrics(data.dashboard);
        
        await new Promise(resolve => setTimeout(resolve, interval));
    }
}

startPolling(5000); // Poll every 5 seconds
```

### 2. React Component

```jsx
import React, { useEffect, useState } from 'react';

function BTPay() {
    const [data, setData] = useState(null);
    
    useEffect(() => {
        const interval = setInterval(async () => {
            const res = await fetch('/finance/api/bt-pay/dashboard/');
            const json = await res.json();
            setData(json.dashboard);
        }, 5000);
        
        return () => clearInterval(interval);
    }, []);
    
    if (!data) return <div>Loading...</div>;
    
    return (
        <div>
            <h2>Pending: {data.pending_count}</h2>
            <p>Today: {data.today_amount.toFixed(2)} RON</p>
        </div>
    );
}

export default BTPay;
```

### 3. Server-Sent Events (SSE)

```html
<div id="metrics"></div>

<script>
const source = new EventSource('/finance/api/bt-pay/stream/?interval=5&duration=600');

source.onmessage = (event) => {
    const data = JSON.parse(event.data);
    document.getElementById('metrics').innerHTML = `
        <p>Pending: ${data.pending_bt_pay}</p>
        <p>Today: ${data.today_amount.toFixed(2)} RON</p>
    `;
};

source.onerror = () => {
    console.error('Connection lost');
    source.close();
};
</script>
```

### 4. Python Requests

```python
import requests
import time

while True:
    response = requests.get(
        'http://localhost:8000/finance/api/bt-pay/dashboard/',
        headers={'Authorization': 'Bearer YOUR_TOKEN'}
    )
    
    data = response.json()['dashboard']
    print(f"Pending: {data['pending_count']}")
    print(f"Today: {data['today_amount']:.2f} RON")
    
    time.sleep(5)  # Poll every 5 seconds
```

### 5. Curl Automation

```bash
#!/bin/bash

# Continuous monitoring
while true; do
    echo "=== BT Pay Stats ==="
    curl -s http://localhost:8000/finance/api/bt-pay/stats/ | jq '.stats'
    echo ""
    sleep 5
done
```

---

## Performance Metrics

| Endpoint | Response Time | Data Points |
|----------|---------------|-------------|
| `/api/bt-pay/transactions/` | 50-100ms | 50 max |
| `/api/bt-pay/stats/` | 100-200ms | 10 |
| `/api/bt-pay/pending/` | 50-100ms | 20 max |
| `/api/bt-pay/dashboard/` | 150-300ms | 100+ |
| `/api/bt-pay/stream/` | 0ms (streaming) | Continuous |
| `/api/bt-pay/hourly/` | 100-150ms | 24 |
| `/api/bt-pay/categories/` | 100-150ms | 10+ |

---

## Error Handling

All endpoints return JSON with status:

**Success:**
```json
{
  "success": true,
  "data": {...},
  "timestamp": "..."
}
```

**Error:**
```json
{
  "success": false,
  "error": "Not authenticated",
  "timestamp": "..."
}
```

**Common errors:**
- `401 Unauthorized` - Not logged in
- `403 Forbidden` - No permission
- `500 Internal Server Error` - Server error

---

## Rate Limiting

No rate limiting on API endpoints. Recommended:
- Polling: 1 request per 5-10 seconds
- SSE stream: Continuous
- Peak load: 1 request per second max

---

## Authentication

All endpoints require Django session authentication:

```bash
# Must be logged in via browser or Django session
curl -b "sessionid=xxx" http://localhost:8000/finance/api/bt-pay/dashboard/
```

---

## WebSocket Support (Future)

Coming soon:
- Real-time WebSocket connection
- Sub-second latency
- Push notifications
- Persistent connection

---

## Debugging

Enable verbose logging:

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'finance.bt_pay_realtime': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

## Links

- **Live Dashboard:** [/finance/bt-pay/](/finance/bt-pay/)
- **API Test:** Use any REST client (Postman, Insomnia, etc.)
- **Documentation:** [BT_PAY_INTEGRATION_GUIDE.md](BT_PAY_INTEGRATION_GUIDE.md)
