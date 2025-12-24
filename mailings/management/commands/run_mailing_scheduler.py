import time
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job

from mailings.services import send_due_mailings


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Команда: python manage.py run_mailing_scheduler
    """

    help = "Запускает планировщик автоматической отправки рассылок."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

        # Хранилище для джобов в БД Django
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Планирование задач
        @register_job(scheduler, "interval", minutes=1, replace_existing=True)
        def job_send_due_mailings():
            logger.info("Проверяем рассылки для автоматической отправки.")
            send_due_mailings()

        scheduler.start()
        logger.info("Планировщик запущен.")

        # Держим процесс активным
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info("Остановка планировщика.")
            scheduler.shutdown()
