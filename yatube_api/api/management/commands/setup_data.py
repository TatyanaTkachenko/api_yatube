from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Group


class Command(BaseCommand):
    help = "Создание тестовых данных: пользователей и группы"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Создание суперпользователя
        admin, _ = User.objects.get_or_create(username="root")
        admin.is_superuser = True
        admin.is_staff = True
        admin.email = "root@admin.ru"
        admin.set_password("5eCretPaSsw0rD")
        admin.save()

        # Создание обычного пользователя
        user, _ = User.objects.get_or_create(username="regular_user")
        user.is_superuser = False
        user.is_staff = False
        user.email = "user@not-admin.ru"
        user.set_password("iWannaBeAdmin")
        user.save()

        # Создание тестовой группы
        Group.objects.get_or_create(
            title="TestGroup", slug="test-group", description="Some text."
        )

        self.stdout.write(self.style.SUCCESS("Setup done."))
