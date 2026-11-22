#!/usr/bin/env python3
"""
RAJA SHADOW - Browser Sandbox

This module is intentionally inert by default. It does not install packages,
send chat messages, call webhooks, or log in to services. If Selenium is
already installed and a human explicitly opts in, it can open a public HTTPS
page for visual inspection.
"""

import ipaddress
import socket
from urllib.parse import urlsplit


class WebPossession:
    """Optional, read-only browser page opener. Disabled unless enabled=True."""

    def __init__(self, headless=True, enabled=False):
        self.headless = headless
        self.enabled = enabled
        self.driver = None

    def init_driver(self):
        if not self.enabled:
            print("Browser sandbox is disabled. Construct with enabled=True to opt in.")
            return False
        if self.driver:
            return True

        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            options = Options()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            self.driver = webdriver.Chrome(options=options)
            return True
        except ImportError:
            print("Selenium is not installed. No package was installed automatically.")
        except Exception as error:
            print(f"Browser could not start: {error}")
        return False

    @staticmethod
    def _validate_url(url):
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("Only public HTTPS pages are supported.")
        host = parsed.hostname.lower().rstrip(".")
        if parsed.username or parsed.password:
            raise ValueError("URLs containing embedded credentials are not allowed.")
        try:
            addresses = {ipaddress.ip_address(host)}
        except ValueError:
            try:
                addresses = {
                    ipaddress.ip_address(item[4][0])
                    for item in socket.getaddrinfo(host, 443)
                }
            except OSError as error:
                raise ValueError(f"Hostname could not be resolved: {error}") from error
        if not addresses or any(not address.is_global for address in addresses):
            raise ValueError("Private, local, and reserved network addresses are blocked.")
        return url

    def open_page(self, url):
        """Open a page for viewing only. No forms are filled or submitted."""
        if not self.enabled:
            print("Browser sandbox is disabled; no browser was opened.")
            return False
        try:
            safe_url = self._validate_url(url)
            if not self.driver and not self.init_driver():
                return False
            self.driver.get(safe_url)
            return True
        except Exception as error:
            print(f"Page could not be opened: {error}")
            return False

    def vanish(self):
        """Close the browser session."""
        if self.driver:
            self.driver.quit()
            self.driver = None
