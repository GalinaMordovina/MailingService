from django.conf import settings
from django.core.mail import send_mail

from .models import Attempt, Mailing


def send_mailing(mailing: Mailing) -> None:
    """
    Отправка писем по рассылке и создание записей Attempt.
    """
    clients = mailing.clients.all()
    subject = mailing.message.subject
    body = mailing.message.body
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')

    # Пометим как запущенную
    if mailing.status == Mailing.STATUS_CREATED:
        mailing.status = Mailing.STATUS_STARTED
        mailing.save()

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
            else:
                Attempt.objects.create(
                    mailing=mailing,
                    status=Attempt.STATUS_FAILED,
                    server_response='send_mail вернул 0 (письмо не отправлено)'
                )
        except Exception as e:
            Attempt.objects.create(
                mailing=mailing,
                status=Attempt.STATUS_FAILED,
                server_response=str(e)
            )
