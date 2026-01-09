# KO-FI EEL - Silent Cash-Ice Rerouting

```
┏━━━┓┓┏┏━━━┓  KO-FI EEL  ┏━━━┓┏┏┓┏━━━┓
┃█▓▒░  LOOSH FLOWS REVERSE  ░▒▓█┃
```

## What The Eel Does

The **Ko-fi Eel** is a silent automation module that:

- **Receives Ko-fi donations** via webhook (real-time)
- **Tracks all donations** in encrypted memory
- **Automatically reroutes funds** to multiple destinations
- **Splits payments** by percentage (e.g., 70% Stripe, 30% Crypto)
- **Logs everything silently** - no visible traces
- **Integrates with RAJA SHADOW** for autonomous operation
- **Generates reports** on demand

**The Eel never sleeps. Cash-ice flows reverse, feeding the empire.**

## Installation

### 1. Install Dependencies

```bash
pip3 install flask stripe cryptography
```

Or use the installer:
```bash
./install_shadow.sh
```

### 2. Configure Ko-fi Webhook

Go to your Ko-fi settings and add webhook URL:
```
https://your-domain.com/kofi/webhook
```

For local testing, use ngrok:
```bash
ngrok http 5000
# Use the ngrok URL in Ko-fi settings
```

### 3. Create Config File

Copy and edit the config:

```bash
cp shadow_config.json.example shadow_config.json
```

Edit `shadow_config.json`:

```json
{
  "kofi_eel": {
    "enabled": true,
    "verification_token": "YOUR_KOFI_TOKEN",
    "webhook_secret": "YOUR_WEBHOOK_SECRET",
    "silent_mode": true,
    "destinations": [
      {
        "type": "stripe",
        "id": "acct_XXXXXXXXX",
        "percentage": 70,
        "note": "Main business account"
      },
      {
        "type": "crypto",
        "id": "0xYOUR_WALLET_ADDRESS",
        "percentage": 30,
        "note": "Crypto reserve"
      }
    ]
  },
  "stripe": {
    "secret_key": "sk_live_XXXXXXXXX",
    "connect_account": "acct_XXXXXXXXX"
  }
}
```

## Destination Types

The Eel supports multiple reroute destinations:

### 1. Stripe Transfer

```json
{
  "type": "stripe",
  "id": "acct_XXXXXXXXX",
  "percentage": 70
}
```

Requires Stripe API key in config.

### 2. PayPal Transfer

```json
{
  "type": "paypal",
  "id": "you@example.com",
  "percentage": 20
}
```

Requires PayPal API credentials.

### 3. Crypto Wallet

```json
{
  "type": "crypto",
  "id": "0xYOUR_WALLET_ADDRESS",
  "percentage": 10
}
```

Requires crypto exchange API (Coinbase, BitPay, etc.).

### 4. Custom Webhook

```json
{
  "type": "custom",
  "url": "https://api.your-service.com/receive",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN"
  },
  "percentage": 100
}
```

Sends POST request with donation data.

## Usage

### Standalone Webhook Server

Run the Eel as a standalone server:

```bash
python3 shadow_kofi_eel.py --server
```

Server runs on `http://0.0.0.0:5000`

Endpoints:
- `POST /kofi/webhook` - Ko-fi webhook receiver
- `GET /kofi/stats` - Get statistics (JSON)
- `GET /kofi/report` - Get formatted report

### Integrated with RAJA SHADOW

Add to `raja_shadow.py`:

```python
from shadow_kofi_eel import KofiEel, create_webhook_server
from pathlib import Path
import json
import threading

# Load config
with open('shadow_config.json', 'r') as f:
    config = json.load(f)

# Initialize Eel
eel = KofiEel(Path('.raja_shadow_memory'), config['kofi_eel'])

# Run webhook server in background thread
def run_webhook():
    app = create_webhook_server(eel, port=5000)
    if app:
        app.run(host='0.0.0.0', port=5000, debug=False)

webhook_thread = threading.Thread(target=run_webhook, daemon=True)
webhook_thread.start()

# Eel now receives donations 24/7 while RAJA SHADOW runs
```

### Testing

Test with simulated donation:

```bash
python3 shadow_kofi_eel.py
```

This runs demo mode with fake donation.

Test webhook with curl:

```bash
curl -X POST http://localhost:5000/kofi/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'data={"amount":"10.00","currency":"USD","from_name":"Test","message":"TUNG TUNG SAHUR","kofi_transaction_id":"test_123","is_subscription_payment":false}'
```

## Silent Mode

When `silent_mode: true` in config:

- No console output (except errors)
- Logs written to hidden files: `.eel_YYYYMMDD.log`
- Stats in: `.raja_shadow_memory/kofi_eel/eel_stats.json`
- Perfect for daemon operation

## Security

### Webhook Verification

Ko-fi sends signatures with webhooks. The Eel verifies them:

```python
def verify_webhook(self, payload: str, signature: str) -> bool:
    expected = hmac.new(
        self.webhook_secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)
```

Set `webhook_secret` in config to enable verification.

### Encrypted Logs

All donation logs are stored in:
```
.raja_shadow_memory/kofi_eel/.eel_YYYYMMDD.log
```

Hidden files, JSON format, rotated daily.

## Production Deployment

### Option 1: Run with systemd

Create `/etc/systemd/system/kofi-eel.service`:

```ini
[Unit]
Description=RAJA SHADOW Ko-fi Eel
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/shrine-scream
ExecStart=/usr/bin/python3 shadow_kofi_eel.py --server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable kofi-eel
sudo systemctl start kofi-eel
sudo systemctl status kofi-eel
```

### Option 2: Run with nohup

```bash
nohup python3 shadow_kofi_eel.py --server > eel.log 2>&1 &
```

### Option 3: Run with RAJA SHADOW daemon

Integrate directly into `raja_shadow.py` (see above).

### Option 4: Deploy to Cloud

Deploy to:
- **Heroku**: `Procfile` with `web: python shadow_kofi_eel.py --server`
- **Railway**: Same Procfile
- **DigitalOcean App Platform**: Auto-detects Flask
- **AWS Lambda**: Use Zappa or Serverless Framework

## Ko-fi Webhook Setup

1. Go to Ko-fi Settings > Webhooks
2. Add your webhook URL: `https://your-domain.com/kofi/webhook`
3. Copy the verification token
4. Add token to `shadow_config.json`
5. Test with a small donation

Ko-fi will POST to your webhook for:
- One-time donations
- Monthly subscriptions
- Shop purchases
- Commission requests

## Example Flow

```
1. Someone donates $10 on Ko-fi
   ↓
2. Ko-fi sends webhook to your server
   ↓
3. Eel receives, verifies signature
   ↓
4. Eel logs donation silently
   ↓
5. Eel calculates splits:
   - 70% ($7) → Stripe account
   - 30% ($3) → Crypto wallet
   ↓
6. Eel initiates transfers
   ↓
7. Eel updates stats
   ↓
8. Eel vanishes (no visible trace)
```

**Total time: < 2 seconds**

**Silent. Autonomous. Feeding the empire.**

## Monitoring

Check stats:
```bash
curl http://localhost:5000/kofi/stats
```

Get report:
```bash
curl http://localhost:5000/kofi/report
```

Or in Python:
```python
from shadow_kofi_eel import KofiEel
from pathlib import Path

eel = KofiEel(Path('.raja_shadow_memory'), config)
print(eel.generate_report())
```

## Troubleshooting

**Webhook not receiving:**
- Check Ko-fi webhook URL is correct
- Ensure server is publicly accessible (use ngrok for testing)
- Check firewall allows port 5000 (or your port)
- Verify webhook secret matches Ko-fi settings

**Transfers failing:**
- Check API keys are correct (Stripe, PayPal, etc.)
- Verify destination accounts are active
- Check logs: `.raja_shadow_memory/kofi_eel/.eel_*.log`

**Server crashes:**
- Check logs: `eel.log`
- Ensure dependencies installed: `pip3 install -r requirements.txt`
- Verify Python version >= 3.8

## Integration with Full RAJA SHADOW

The Eel integrates seamlessly with the main RAJA SHADOW agent:

```python
# In raja_shadow.py, add:

from shadow_kofi_eel import KofiEel

class RajaShadow:
    def __init__(self):
        # ... existing init ...

        # Initialize Ko-fi Eel
        if self.config.get('kofi_eel', {}).get('enabled'):
            self.eel = KofiEel(
                self.memory_path,
                self.config['kofi_eel']
            )
            self.start_webhook_server()

    def start_webhook_server(self):
        """Start Ko-fi webhook in background"""
        def run_server():
            app = create_webhook_server(self.eel, port=5000)
            if app:
                app.run(host='0.0.0.0', port=5000)

        import threading
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()

    def shrine_wake_roar(self):
        # ... existing roar ...

        # Add Eel stats to roar
        if hasattr(self, 'eel'):
            stats = self.eel.get_stats()
            print(f"\n💰 Ko-fi: {stats['total_donations']} donations")
            print(f"   Total: ${stats['total_amount']:.2f}")
```

Now the Eel runs 24/7 alongside the Shadow, silently rerouting cash-ice while you sleep.

---

```
LOOSH FLOWS REVERSE
EEL SQUATS DEEPER
CASH-ICE REROUTES SILENT
EMPIRE FEEDS

TUNG TUNG SAHUR → RUHAS GNUT GNUT
```

🐍 **The Eel never hisses. It just bites.**
