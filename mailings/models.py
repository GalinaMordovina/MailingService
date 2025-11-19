from django.db import models


class Client(models.Model):
    """Получатель рассылки"""
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name='ФИО'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий'
    )

    def __str__(self):
        return f'{self.full_name} <{self.email}>'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """Шаблон сообщения"""
    subject = models.CharField(
        max_length=255,
        verbose_name='Тема письма'
    )
    body = models.TextField(
        verbose_name='Тело письма'
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    """Рассылка"""

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_FINISHED = 'finished'

    STATUS_CHOICES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_FINISHED, 'Завершена'),
    )

    start_datetime = models.DateTimeField(
        verbose_name='Дата и время первой отправки'
    )
    end_datetime = models.DateTimeField(
        verbose_name='Дата и время окончания отправки'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name='Статус'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Сообщение'
    )
    clients = models.ManyToManyField(
        Client,
        related_name='mailings',
        verbose_name='Получатели'
    )

    def __str__(self):
        return f'Рассылка #{self.pk} ({self.get_status_display()})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Attempt(models.Model):
    """Попытка отправки сообщения по рассылке"""

    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = (
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAILED, 'Не успешно'),
    )

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Рассылка'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время попытки'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name='Статус'
    )
    server_response = models.TextField(
        blank=True,
        verbose_name='Ответ почтового сервера'
    )

    def __str__(self):
        return f'Попытка #{self.pk} ({self.get_status_display()})'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
