from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import logging

from .models import Attempt, Mailing

logger = logging.getLogger('mailings')


def send_due_mailings():
    """
    Находит все активные рассылки, для которых сейчас время отправки,
    и запускает send_mailing для каждой.
    """
    now = timezone.now()

    # Берём только активные рассылки, у которых "сейчас" внутри окна отправки
    mailings = Mailing.objects.filter(
        is_active=True,
        start_datetime__lte=now,
        end_datetime__gte=now,
    )

    # Дополнительно: не отправляем рассылки заблокированных пользователей (если owner есть в модели Mailing)
    mailings = mailings.filter(owner__is_active=True)

    for mailing in mailings:
        send_mailing(mailing)

        # Если время окончания уже прошло, то считаем рассылку завершённой
        if mailing.end_datetime < timezone.now():
            mailing.status = Mailing.STATUS_FINISHED
            mailing.is_active = False
            mailing.save(update_fields=['status', 'is_active'])
            logger.info(f"Рассылка #{mailing.id} завершена автоматически (по времени).")


def send_mailing(mailing: Mailing) -> None:
    """
    Отправка писем по рассылке и создание записей Attempt.
    """
    logger.info(f"Начинаем отправку рассылки #{mailing.id}")

    # Защита от частых повторов (антиспам планировщика)
    last_attempt = mailing.attempts.order_by('-created_at').first()
    if last_attempt and last_attempt.created_at > timezone.now() - timedelta(minutes=1):
        logger.info(
            f"Рассылка #{mailing.id} уже отправлялась менее минуты назад — пропускаем."
        )
        return

    clients = mailing.clients.all()
    if not clients.exists():
        logger.warning(
            f"У рассылки #{mailing.id} нет получателей; отправка пропущена."
        )
        return

    subject = mailing.message.subject
    body = mailing.message.body
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')

    # Если рассылка только создана, то помечаем как запущенную
    if mailing.status == Mailing.STATUS_CREATED:
        mailing.status = Mailing.STATUS_STARTED
        mailing.save(update_fields=['status'])

    for client in clients:
        try:
            sent_count = send_mail(
                subject,
                body,
                from_email,
                [client.email],
                fail_silently=False,
            )
            if sent_count:
                Attempt.objects.create(
                    mailing=mailing,
                    status=Attempt.STATUS_SUCCESS,
                    server_response='Отправлено успешно'
                )
                logger.info(f"Письмо для {client.email} отправлено успешно")
            else:
                Attempt.objects.create(
                    mailing=mailing,
                    status=Attempt.STATUS_FAILED,
                    server_response='send_mail вернул 0 (письмо не отправлено)'
                )
                logger.error(
                    f"send_mail вернул 0 при отправке для {client.email} "
                    f"в рассылке #{mailing.id}"
                )
        except Exception as e:
            Attempt.objects.create(
                mailing=mailing,
                status=Attempt.STATUS_FAILED,
                server_response=str(e)
            )
            logger.error(f"Ошибка при отправке для {client.email}: {e}")
