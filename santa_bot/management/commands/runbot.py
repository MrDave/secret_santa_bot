from django.core.management.base import BaseCommand
from santa_bot import bot


class Command(BaseCommand):
    help = "Start Telegram bot"

    def handle(self, *args, **options):
        bot.main()
