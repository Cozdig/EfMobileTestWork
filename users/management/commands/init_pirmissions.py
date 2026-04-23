from django.core.management.base import BaseCommand
from users.models import Permission, RolePermission


class Command(BaseCommand):
    help = 'Инициализация прав доступа'

    def handle(self, *args, **options):
        permissions = {
            'can_view_product': 'Просмотр товаров',
            'can_create_product': 'Создание товаров',
            'can_edit_product': 'Редактирование товаров',
            'can_delete_product': 'Удаление товаров',
            'can_view_user': 'Просмотр пользователей',
            'can_edit_user': 'Редактирование пользователей',
            'can_delete_user': 'Удаление пользователей',
            'can_manage_roles': 'Управление ролями и правами',
        }

        for codename, name in permissions.items():
            Permission.objects.get_or_create(codename=codename, defaults={'name': name})

        role_permissions = {
            'admin': [
                'can_view_product', 'can_create_product', 'can_edit_product', 'can_delete_product',
                'can_view_user', 'can_edit_user', 'can_delete_user', 'can_manage_roles'
            ],
            'manager': [
                'can_view_product', 'can_create_product', 'can_edit_product',
                'can_view_user',
            ],
            'user': [
                'can_view_product',
            ],
        }

        for role, perms in role_permissions.items():
            for perm_codename in perms:
                perm = Permission.objects.get(codename=perm_codename)
                RolePermission.objects.get_or_create(role=role, permission=perm)

        self.stdout.write(self.style.SUCCESS('Права доступа инициализированы'))