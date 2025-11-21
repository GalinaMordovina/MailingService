from django.core.management.base import BaseCommand
from mailings.services import send_due_mailings


class Command(BaseCommand):
    """
    Кастомная команда для запуска рассылок из командной строки.

    Использование:
        python manage.py send_mailings
    """

    help = 'Отправка всех подходящих по времени активных рассылок'

    def handle(self, *args, **options):
        self.stdout.write('Запуск отправки рассылок...')
        send_due_mailings()
        self.stdout.write(self.style.SUCCESS('Отправка рассылок завершена.'))
