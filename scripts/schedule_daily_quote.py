import os
import sys
import threading

def run_send_daily_quote_command():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PulsePoint.settings")
    from django.core.management import call_command
    call_command("send_daily_quote")

def main():
    # Schedule the send_daily_quote command to run every 24 hours
    while True:
        run_send_daily_quote_command()
        time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    thread = threading.Thread(target=main)
    thread.start()
