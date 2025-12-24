from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from mailings.models import Client, Message, Mailing


class Command(BaseCommand):
    """
    Команда для создания группы «Менеджеры» и назначения ей прав.

    Использование:
        python manage.py init_managers
    """

    help = 'Создаёт группу "Менеджеры" и назначает ей необходимые права.'

    def handle(self, *args, **options):
        group_name = 'Менеджеры'

        managers_group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана.'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа "{group_name}" уже существует.'))

        # Права на модели рассылок-приложения mailings

        client_ct = ContentType.objects.get_for_model(Client)
        message_ct = ContentType.objects.get_for_model(Message)
        mailing_ct = ContentType.objects.get_for_model(Mailing)

        perms_codenames = [
            # из Meta Client
            ('can_view_all_clients', client_ct),
            # из Meta Message
            ('can_view_all_messages', message_ct),
            # из Meta Mailing
            ('can_view_all_mailings', mailing_ct),
            ('can_disable_mailings', mailing_ct),
        ]

        for codename, ct in perms_codenames:
            try:
                perm = Permission.objects.get(content_type=ct, codename=codename)
                managers_group.permissions.add(perm)
                self.stdout.write(self.style.SUCCESS(f'Добавлено право: {codename}'))
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f'Право с codename="{codename}" для {ct} не найдено. '
                        f'Убедитесь, что миграции применены.'
                    )
                )

        # Дополнительно: права на пользователей (чтобы менеджер мог смотреть и блокировать)

        try:
            user_perms = Permission.objects.filter(
                content_type__app_label='auth',
                content_type__model='user',
                codename__in=['view_user', 'change_user'],
            )
            for perm in user_perms:
                managers_group.permissions.add(perm)
                self.stdout.write(self.style.SUCCESS(f'Добавлено право: {perm.codename} (auth.user)'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при добавлении прав для пользователей: {e}'))

        self.stdout.write(self.style.SUCCESS('Настройка группы "Менеджеры" завершена.'))
