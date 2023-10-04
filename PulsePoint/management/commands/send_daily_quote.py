from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.auth.models import User
import requests
import time


class Command(BaseCommand):
    help = "Send a daily quote to registered users."

    def send_daily_quote(self, *args, **kwargs):
        api_url = "https://zenquotes.io/api/random"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            quote = data[0]["q"]
            users = User.objects.filter(is_active=True)
            for user in users:
                subject = "Quote of the Day"
                message = f"Here's your quote of the day.:\n\n{quote}"
                from_email = "pulsepointregister@gmail.com"
                recipent_email = user.email
                send_mail(subject, message, from_email, [recipent_email])
        else:
            self.stdout.write(self.style.ERROR("Failed to fetch a quote from the API."))

    def handle(self, *args, **options):
        while True:
            self.send_daily_quote()
            time.sleep(24 * 60 * 60)
