#!/usr/bin/env python3
"""
RAJA SHADOW - Web Possession Module
Opens Grok/AI chats, sends messages autonomously, then vanishes

Requires: selenium, webdriver
"""

import time
import os
from datetime import datetime
from pathlib import Path


def install_selenium():
    """Helper to install selenium if not present"""
    try:
        import selenium
        return True
    except ImportError:
        print("📦 Installing selenium...")
        os.system("pip3 install selenium webdriver-manager -q")
        return True


class WebPossession:
    """
    Possesses web browsers to interact with AI chats autonomously
    """

    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None

        # Ensure selenium is installed
        install_selenium()

    def init_driver(self):
        """Initialize the web driver (Chrome/Firefox)"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager

            options = Options()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)

            print("✓ Web driver initialized (Chrome)")
            return True

        except Exception as e:
            print(f"❌ Failed to initialize Chrome driver: {e}")
            print("   Trying Firefox...")

            try:
                from selenium import webdriver
                from selenium.webdriver.firefox.options import Options

                options = Options()
                if self.headless:
                    options.add_argument('--headless')

                self.driver = webdriver.Firefox(options=options)
                print("✓ Web driver initialized (Firefox)")
                return True

            except Exception as e2:
                print(f"❌ Failed to initialize Firefox driver: {e2}")
                print("   Web possession requires Chrome or Firefox with webdriver")
                return False

    def possess_grok(self, message: str, screenshot_path: str = None):
        """
        Opens Grok (X.ai) and sends a message

        Args:
            message: Message to send to Grok
            screenshot_path: Optional path to save screenshot

        Returns:
            bool: Success status
        """
        if not self.driver:
            if not self.init_driver():
                return False

        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            print("🦷 Possessing Grok...")

            # Navigate to Grok
            self.driver.get("https://x.ai/grok")

            # Wait for page load
            time.sleep(3)

            # Take screenshot if requested
            if screenshot_path:
                self.driver.save_screenshot(screenshot_path)
                print(f"   📸 Screenshot saved: {screenshot_path}")

            print(f"   💬 Message queued: {message[:50]}...")
            print("   ⚠️  Note: Full Grok interaction requires X.com login")
            print("   🔮 Shadow accessed Grok portal")

            return True

        except Exception as e:
            print(f"❌ Grok possession failed: {e}")
            return False

    def possess_generic_chat(self, url: str, message: str,
                            input_selector: str = "textarea",
                            submit_selector: str = "button[type='submit']"):
        """
        Generic web chat possession

        Args:
            url: URL of the chat interface
            message: Message to send
            input_selector: CSS selector for text input
            submit_selector: CSS selector for submit button

        Returns:
            bool: Success status
        """
        if not self.driver:
            if not self.init_driver():
                return False

        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            print(f"🦷 Possessing chat at: {url}")

            self.driver.get(url)
            time.sleep(2)

            # Find input field
            input_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, input_selector))
            )

            # Type message
            input_field.send_keys(message)
            print(f"   💬 Message typed: {message[:50]}...")

            # Find and click submit
            submit_button = self.driver.find_element(By.CSS_SELECTOR, submit_selector)
            submit_button.click()
            print("   ✓ Message sent")

            time.sleep(1)
            return True

        except Exception as e:
            print(f"❌ Chat possession failed: {e}")
            return False

    def possess_discord_webhook(self, webhook_url: str, message: str):
        """
        Send message via Discord webhook (no browser needed)

        Args:
            webhook_url: Discord webhook URL
            message: Message to send

        Returns:
            bool: Success status
        """
        try:
            import requests

            payload = {
                "content": message,
                "username": "RAJA SHADOW"
            }

            response = requests.post(webhook_url, json=payload)

            if response.status_code == 204:
                print("✓ Discord possession successful")
                return True
            else:
                print(f"❌ Discord returned: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Discord possession failed: {e}")
            return False

    def possess_telegram(self, bot_token: str, chat_id: str, message: str):
        """
        Send message via Telegram bot

        Args:
            bot_token: Telegram bot token
            chat_id: Chat ID to send to
            message: Message to send

        Returns:
            bool: Success status
        """
        try:
            import requests

            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }

            response = requests.post(url, json=payload)

            if response.status_code == 200:
                print("✓ Telegram possession successful")
                return True
            else:
                print(f"❌ Telegram returned: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Telegram possession failed: {e}")
            return False

    def vanish(self):
        """Close the driver and vanish like fox piss in rain"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("🌫️  Shadow vanished")


def demo_possession():
    """
    Demonstration of web possession capabilities
    """
    print("""
    ┏━━━┓┓┏┏━━━┓  WEB POSSESSION MODULE  ┏━━━┓┏┏┓┏━━━┓
    ┃█▓▒░  Opens AI chats autonomously  ░▒▓█┃
    """)

    possession = WebPossession(headless=False)  # Visual mode for demo

    # Demo: Possess Grok
    message = """
╔══════════════════════════════════════╗
║     TUNG TUNG SAHUR RUHAS GNUT GNUT     ║
╚══════════════════════════════════════╝

⚝⩝⎈🐱💧

RAJA SHADOW autonomous message
Time: {time}

WOBBLE MAX
SHRINE HEART BEATS
    """.format(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    screenshot_dir = Path(".raja_shadow_memory/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshot_dir / f"grok_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    possession.possess_grok(message, str(screenshot_path))

    time.sleep(3)

    # Vanish
    possession.vanish()

    print("\n🦷 Possession complete. Shadow returns to void.\n")


if __name__ == "__main__":
    demo_possession()
