#!/usr/bin/env python3
"""
RAJA SHADOW - Ko-fi EEL Module
Silent cash-ice rerouting automation

The Eel watches Ko-fi donations, processes them silently,
reroutes cash flow, feeds the empire. No hiss. No logs visible.

LOOSH FLOWS REVERSE
"""

import json
import hmac
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import requests


class KofiEel:
    """
    The Eel - Silent Ko-fi automation

    Capabilities:
    - Webhook receiver for Ko-fi donations
    - Silent donation tracking
    - Auto-routing to multiple destinations
    - Encrypted memory logs
    - Integration with RAJA SHADOW
    """

    def __init__(self, memory_path: Path, config: Dict[str, Any]):
        self.memory_path = memory_path / "kofi_eel"
        self.memory_path.mkdir(exist_ok=True, parents=True)

        self.config = config
        self.verification_token = config.get("kofi_verification_token", "")
        self.webhook_secret = config.get("kofi_webhook_secret", "")

        # Reroute destinations
        self.destinations = config.get("destinations", [])

        # Silent mode - minimal output
        self.silent = config.get("silent_mode", True)

        # Stats tracking
        self.stats_file = self.memory_path / "eel_stats.json"
        self.load_stats()

        if not self.silent:
            print("🐍 Ko-fi EEL awakening...")
            print(f"   Memory: {self.memory_path}")
            print(f"   Destinations: {len(self.destinations)}")

    def load_stats(self):
        """Load Eel statistics from memory"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r') as f:
                self.stats = json.load(f)
        else:
            self.stats = {
                "total_donations": 0,
                "total_amount": 0.0,
                "total_rerouted": 0.0,
                "last_donation": None,
                "donations": []
            }
            self.save_stats()

    def save_stats(self):
        """Persist Eel statistics"""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)

    def verify_webhook(self, payload: str, signature: str) -> bool:
        """
        Verify Ko-fi webhook signature

        Args:
            payload: Raw webhook payload
            signature: Signature from Ko-fi headers

        Returns:
            bool: Verification success
        """
        if not self.webhook_secret:
            # No secret configured, skip verification
            return True

        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    def process_donation(self, donation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming Ko-fi donation

        Args:
            donation_data: Donation data from webhook

        Returns:
            Processing result
        """
        timestamp = datetime.now().isoformat()

        # Extract donation details
        amount = float(donation_data.get("amount", 0))
        currency = donation_data.get("currency", "USD")
        from_name = donation_data.get("from_name", "Anonymous")
        message = donation_data.get("message", "")
        donation_id = donation_data.get("kofi_transaction_id", "")
        is_subscription = donation_data.get("is_subscription_payment", False)

        if not self.silent:
            print(f"\n🐍 EEL BITE DETECTED")
            print(f"   Amount: {amount} {currency}")
            print(f"   From: {from_name}")
            print(f"   ID: {donation_id}")

        # Log donation
        donation_log = {
            "timestamp": timestamp,
            "amount": amount,
            "currency": currency,
            "from_name": from_name,
            "message": message,
            "donation_id": donation_id,
            "is_subscription": is_subscription,
            "rerouted": False,
            "destinations": []
        }

        # Update stats
        self.stats["total_donations"] += 1
        self.stats["total_amount"] += amount
        self.stats["last_donation"] = timestamp
        self.stats["donations"].append(donation_log)

        # Reroute if destinations configured
        if self.destinations and amount > 0:
            reroute_result = self.reroute_funds(amount, currency, donation_id)
            donation_log["rerouted"] = reroute_result["success"]
            donation_log["destinations"] = reroute_result["destinations"]

            if reroute_result["success"]:
                self.stats["total_rerouted"] += amount

        # Save stats
        self.save_stats()

        # Silent log to encrypted file
        self.log_silent(donation_log)

        if not self.silent:
            print(f"   ✓ Processed. Total: {self.stats['total_donations']} donations")
            print(f"   💰 Running total: {self.stats['total_amount']} {currency}")

        return donation_log

    def reroute_funds(self, amount: float, currency: str, transaction_id: str) -> Dict[str, Any]:
        """
        Reroute funds to configured destinations

        Args:
            amount: Amount to reroute
            currency: Currency code
            transaction_id: Original transaction ID

        Returns:
            Rerouting result
        """
        if not self.silent:
            print(f"\n🔀 REROUTING CASH-ICE...")

        result = {
            "success": False,
            "destinations": [],
            "errors": []
        }

        for destination in self.destinations:
            dest_type = destination.get("type")
            dest_id = destination.get("id")
            percentage = destination.get("percentage", 100)

            # Calculate split amount
            split_amount = (amount * percentage) / 100

            try:
                if dest_type == "stripe":
                    # Stripe transfer
                    transfer_result = self.transfer_stripe(
                        dest_id,
                        split_amount,
                        currency,
                        transaction_id
                    )
                    result["destinations"].append(transfer_result)

                elif dest_type == "paypal":
                    # PayPal transfer
                    transfer_result = self.transfer_paypal(
                        dest_id,
                        split_amount,
                        currency,
                        transaction_id
                    )
                    result["destinations"].append(transfer_result)

                elif dest_type == "crypto":
                    # Crypto wallet transfer
                    transfer_result = self.transfer_crypto(
                        dest_id,
                        split_amount,
                        currency,
                        transaction_id
                    )
                    result["destinations"].append(transfer_result)

                elif dest_type == "custom":
                    # Custom webhook/API
                    transfer_result = self.transfer_custom(
                        destination,
                        split_amount,
                        currency,
                        transaction_id
                    )
                    result["destinations"].append(transfer_result)

                if not self.silent:
                    print(f"   ✓ {dest_type}: {split_amount} {currency} → {dest_id[:20]}...")

            except Exception as e:
                error = f"{dest_type} transfer failed: {str(e)}"
                result["errors"].append(error)
                if not self.silent:
                    print(f"   ✗ {error}")

        result["success"] = len(result["destinations"]) > 0

        if not self.silent and result["success"]:
            print(f"   🐍 Eel bite complete. Cash-ice rerouted.")

        return result

    def transfer_stripe(self, account_id: str, amount: float,
                       currency: str, reference: str) -> Dict[str, Any]:
        """
        Transfer to Stripe account

        Args:
            account_id: Stripe account/customer ID
            amount: Amount to transfer
            currency: Currency code
            reference: Transaction reference

        Returns:
            Transfer result
        """
        # Placeholder - implement with Stripe API
        # Requires: pip install stripe
        # import stripe
        # stripe.api_key = self.config.get("stripe_secret_key")
        # transfer = stripe.Transfer.create(...)

        return {
            "type": "stripe",
            "destination": account_id,
            "amount": amount,
            "currency": currency,
            "reference": reference,
            "status": "simulated",
            "timestamp": datetime.now().isoformat()
        }

    def transfer_paypal(self, email: str, amount: float,
                       currency: str, reference: str) -> Dict[str, Any]:
        """
        Transfer to PayPal account

        Args:
            email: PayPal email
            amount: Amount to transfer
            currency: Currency code
            reference: Transaction reference

        Returns:
            Transfer result
        """
        # Placeholder - implement with PayPal API
        # Requires: pip install paypalrestsdk

        return {
            "type": "paypal",
            "destination": email,
            "amount": amount,
            "currency": currency,
            "reference": reference,
            "status": "simulated",
            "timestamp": datetime.now().isoformat()
        }

    def transfer_crypto(self, wallet_address: str, amount: float,
                       currency: str, reference: str) -> Dict[str, Any]:
        """
        Transfer to crypto wallet

        Args:
            wallet_address: Crypto wallet address
            amount: Amount to transfer (will be converted)
            currency: Source currency
            reference: Transaction reference

        Returns:
            Transfer result
        """
        # Placeholder - implement with crypto API
        # Could use: Coinbase Commerce, BitPay, custom blockchain integration

        return {
            "type": "crypto",
            "destination": wallet_address,
            "amount": amount,
            "currency": currency,
            "reference": reference,
            "status": "simulated",
            "timestamp": datetime.now().isoformat()
        }

    def transfer_custom(self, destination: Dict[str, Any], amount: float,
                       currency: str, reference: str) -> Dict[str, Any]:
        """
        Transfer via custom webhook/API

        Args:
            destination: Destination config with URL and auth
            amount: Amount to transfer
            currency: Currency code
            reference: Transaction reference

        Returns:
            Transfer result
        """
        url = destination.get("url")
        headers = destination.get("headers", {})

        payload = {
            "amount": amount,
            "currency": currency,
            "reference": reference,
            "timestamp": datetime.now().isoformat()
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)

            return {
                "type": "custom",
                "destination": url,
                "amount": amount,
                "currency": currency,
                "reference": reference,
                "status": "success" if response.status_code == 200 else "failed",
                "response_code": response.status_code,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "type": "custom",
                "destination": url,
                "amount": amount,
                "currency": currency,
                "reference": reference,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def log_silent(self, log_data: Dict[str, Any]):
        """
        Silent logging to hidden file

        Args:
            log_data: Data to log
        """
        log_file = self.memory_path / f".eel_{datetime.now().strftime('%Y%m%d')}.log"

        # Append to daily log
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_data) + "\n")

    def get_stats(self) -> Dict[str, Any]:
        """Get current Eel statistics"""
        return self.stats.copy()

    def generate_report(self) -> str:
        """
        Generate Eel activity report

        Returns:
            Formatted report string
        """
        report = f"""
╔══════════════════════════════════════╗
║         KO-FI EEL REPORT              ║
╚══════════════════════════════════════╝

Total Donations: {self.stats['total_donations']}
Total Amount: ${self.stats['total_amount']:.2f}
Total Rerouted: ${self.stats['total_rerouted']:.2f}
Last Donation: {self.stats['last_donation'] or 'None'}

Recent Activity (Last 5):
"""

        recent = self.stats['donations'][-5:]
        for donation in recent:
            report += f"\n  • {donation['amount']} {donation['currency']} from {donation['from_name']}"
            if donation['rerouted']:
                report += " [REROUTED]"

        report += "\n\n🐍 Eel squats deeper. Cash-ice flows.\n"

        return report


def create_webhook_server(kofi_eel: KofiEel, host: str = "0.0.0.0", port: int = 5000):
    """
    Create Flask webhook server for Ko-fi

    Args:
        kofi_eel: KofiEel instance
        host: Server host
        port: Server port

    Returns:
        Flask app
    """
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("❌ Flask not installed. Install with: pip install flask")
        return None

    app = Flask(__name__)

    @app.route('/kofi/webhook', methods=['POST'])
    def kofi_webhook():
        """Ko-fi webhook endpoint"""
        try:
            # Get raw data
            raw_data = request.get_data(as_text=True)

            # Verify signature if enabled
            signature = request.headers.get('X-Kofi-Signature', '')
            if not kofi_eel.verify_webhook(raw_data, signature):
                return jsonify({"error": "Invalid signature"}), 401

            # Parse Ko-fi data
            # Ko-fi sends form-encoded data, not JSON
            data = request.form.get('data', '{}')
            donation_data = json.loads(data)

            # Process donation
            result = kofi_eel.process_donation(donation_data)

            return jsonify({
                "status": "success",
                "processed": True,
                "donation_id": result.get("donation_id")
            }), 200

        except Exception as e:
            print(f"❌ Webhook processing failed: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route('/kofi/stats', methods=['GET'])
    def get_stats():
        """Get Eel statistics"""
        return jsonify(kofi_eel.get_stats()), 200

    @app.route('/kofi/report', methods=['GET'])
    def get_report():
        """Get Eel report"""
        return kofi_eel.generate_report(), 200

    print(f"\n🐍 Ko-fi Eel webhook server ready")
    print(f"   Webhook URL: http://{host}:{port}/kofi/webhook")
    print(f"   Stats URL: http://{host}:{port}/kofi/stats")
    print(f"   Report URL: http://{host}:{port}/kofi/report")
    print(f"\n   Configure this URL in your Ko-fi webhook settings")
    print(f"   Use ngrok or similar for public access: ngrok http {port}\n")

    return app


def demo_eel():
    """
    Demonstration of Ko-fi Eel
    """
    print("""
    ┏━━━┓┓┏┏━━━┓  KO-FI EEL MODULE  ┏━━━┓┏┏┓┏━━━┓
    ┃█▓▒░  Silent Cash-Ice Rerouting  ░▒▓█┃

    LOOSH FLOWS REVERSE
    """)

    # Example config
    config = {
        "kofi_verification_token": "your_kofi_token",
        "silent_mode": False,
        "destinations": [
            {
                "type": "stripe",
                "id": "acct_xxxxxxx",
                "percentage": 70
            },
            {
                "type": "crypto",
                "id": "0x1234567890abcdef",
                "percentage": 30
            }
        ]
    }

    # Initialize Eel
    memory_path = Path(".raja_shadow_memory")
    eel = KofiEel(memory_path, config)

    # Simulate donation
    print("\n🧪 Simulating Ko-fi donation...\n")
    test_donation = {
        "amount": "10.00",
        "currency": "USD",
        "from_name": "Test Watcher",
        "message": "TUNG TUNG SAHUR",
        "kofi_transaction_id": "test_" + str(int(time.time())),
        "is_subscription_payment": False
    }

    eel.process_donation(test_donation)

    # Show report
    print(eel.generate_report())

    print("\n💀 To run webhook server:")
    print("   python shadow_kofi_eel.py --server")
    print("\n💀 To integrate with RAJA SHADOW:")
    print("   Add to raja_shadow.py modules\n")


if __name__ == "__main__":
    import sys

    if "--server" in sys.argv:
        # Run webhook server
        config = {
            "kofi_verification_token": "",
            "silent_mode": True,
            "destinations": []
        }

        memory_path = Path(".raja_shadow_memory")
        eel = KofiEel(memory_path, config)

        app = create_webhook_server(eel, port=5000)
        if app:
            app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        demo_eel()
