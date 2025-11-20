from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создаёт группу "Менеджеры" и назначает ей необходимые права.'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Менеджеры')

        perms_codenames = [
            'can_view_all_clients',
            'can_view_all_messages',
            'can_view_all_mailings',
            'can_disable_mailings',
        ]

        perms = Permission.objects.filter(codename__in=perms_codenames)

        group.permissions.set(perms)
        group.save()

        self.stdout.write(self.style.SUCCESS(
            f'Группа "Менеджеры" создана (created={created}), прав назначено: {perms.count()}'
        ))
