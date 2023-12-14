from django.core.management.base import BaseCommand

from santa_bot.bot.bot import main


class Command(BaseCommand):
    help = 'Runs the telegram bot'

    def handle(self, *args, **options):
        main()
