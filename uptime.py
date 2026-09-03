#!/usr/bin/env python3
"""
Uptime monitor for wang-guangxin.github.io

Reads site list from sites.json, checks HTTP status & SSL expiry,
computes 7-day / 24h uptime from data.csv history, and writes a
clean JSON data file consumed by the Vue frontend.

Usage:
    python3 uptime.py
"""

import csv
import json
import os
import socket
import ssl
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from urllib.parse import urlparse

import pytz
import requests
from requests import exceptions

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SITES_FILE = "sites.json"
DATA_FILE = "data.csv"
OUTPUT_FILE = "static/sites-data.json"
HISTORY_DAYS = 7
SSL_WARN_DAYS = 15  # warn when SSL cert expires within this many days

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_sites():
    with open(SITES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["sites"]


def load_history():
    """Load CSV history into a dict: url -> list of (timestamp, is_up)."""
    history = defaultdict(list)
    if not os.path.exists(DATA_FILE):
        return history
    cutoff = datetime.now() - timedelta(days=HISTORY_DAYS)
    with open(DATA_FILE, "r", newline="") as f:
        for row in csv.reader(f):
            if len(row) < 3:
                continue
            ts, url, is_up = row[0], row[1], row[2]
            try:
                t = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            if t >= cutoff:
                history[url].append((t, is_up == "True"))
    return history


def save_history(history):
    rows = []
    for url, entries in history.items():
        for t, is_up in entries:
            rows.append([t.strftime("%Y-%m-%d %H:%M:%S"), url, str(is_up)])
    rows.sort(key=lambda r: r[0])
    with open(DATA_FILE, "w", newline="") as f:
        csv.writer(f).writerows(rows)


def check_http(url, timeout=10):
    try:
        return requests.get(url, timeout=timeout).status_code == 200
    except exceptions.RequestException:
        return False


def check_ssl(url):
    """Return days until SSL cert expiry, or None if unavailable."""
    try:
        host = urlparse(url).hostname
        port = urlparse(url).port or 443
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host) as s:
            s.settimeout(5)
            s.connect((host, port))
            cert = s.getpeercert()
        not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        return (not_after - datetime.utcnow()).days
    except Exception:
        return None


def uptime_pct(entries, since=None):
    if not entries:
        return None
    if since is not None:
        entries = [e for e in entries if e[0] >= since]
    if not entries:
        return None
    up = sum(1 for _, is_up in entries if is_up)
    return round(up / len(entries) * 100, 2)


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------
def send_notice(title, body):
    host = os.environ.get("notice_host_server")
    user = os.environ.get("notice_user")
    pwd = os.environ.get("notice_pwd")
    mail = os.environ.get("notice_mail")
    receiver = os.environ.get("notice_receiver")
    if not all([host, user, pwd, mail, receiver]):
        print("[notice] SMTP env vars missing, skip notification")
        return
    msg = MIMEText(body, "html", "utf-8")
    msg["Subject"] = Header(title, "utf-8")
    msg["From"] = mail
    msg["To"] = receiver
    with SMTP_SSL(host) as smtp:
        smtp.login(user, pwd)
        smtp.sendmail(mail, receiver, msg.as_string())
    print("[notice] notification sent")


def notify_changes(prev, curr):
    """Compare previous run's status with current, send email on changes.

    Sends an email when:
      1. A site's up/down status changed since last run.
      2. A site's SSL cert crossed into the warning zone (<= SSL_WARN_DAYS).
    """
    # No baseline yet (first run / fresh checkout) — skip to avoid false alarms.
    if not prev:
        print("[notice] no previous baseline, skip change notification")
        return

    changes = []
    ssl_warnings = []

    for site in curr:
        url = site["url"]
        old = prev.get(url)

        # 1. Status change detection
        if old is not None and old["up"] != site["up"]:
            state = "🟢 Up" if site["up"] else "🔴 Down"
            changes.append(f"<p><a href='{url}'>{site['name']}</a> → {state}</p>")

        # 2. SSL expiry warning (only when crossing into the warning zone)
        days = site["ssl_days"]
        old_days = old.get("ssl_days") if old else None
        if days is not None and days <= SSL_WARN_DAYS:
            if old_days is None or old_days > SSL_WARN_DAYS:
                ssl_warnings.append(
                    f"<p><a href='{url}'>{site['name']}</a> — "
                    f"SSL expires in <strong>{days} days</strong> ⚠️</p>"
                )

    if not changes and not ssl_warnings:
        return

    body = ""
    if changes:
        body += "<h2>Status Changed</h2>" + "".join(changes)
    if ssl_warnings:
        body += "<h2>SSL Warning</h2>" + "".join(ssl_warnings)
    body += "<p><a href='https://wang-guangxin.github.io/sites'>View all sites</a></p>"
    send_notice(f"Uptime Report {now_str()}", body)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    sites = load_sites()
    history = load_history()
    now = datetime.now()
    day_ago = now - timedelta(days=1)

    results = []
    for site in sites:
        url = site["url"]
        up = check_http(url)
        ssl_days = check_ssl(url)
        history[url].append((now, up))
        # keep only last 7 days
        history[url] = [e for e in history[url] if e[0] >= now - timedelta(days=HISTORY_DAYS)]

        results.append({
            "name": site["name"],
            "url": url,
            "badges": site.get("badges", []),
            "up": up,
            "ssl_days": ssl_days,
            "uptime_7d": uptime_pct(history[url]),
            "uptime_24h": uptime_pct(history[url], since=day_ago),
        })

    save_history(history)

    # Load previous status for change detection
    prev = {}
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                prev = {s["url"]: s for s in json.load(f)["sites"]}
        except (json.JSONDecodeError, KeyError):
            prev = {}

    payload = {
        "updated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at_cst": datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S"),
        "sites": results,
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"[ok] wrote {OUTPUT_FILE} with {len(results)} sites")

    if os.environ.get("NOTICE_ENABLED", "1") == "1":
        notify_changes(prev, results)


if __name__ == "__main__":
    sys.exit(main())
