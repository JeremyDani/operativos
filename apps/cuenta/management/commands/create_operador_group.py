from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = (
        "Create or update the 'operador' group. This group is intended for users "
        "who only use the frontend SPA; it will not grant admin/staff privileges."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--user",
            dest="username",
            help="(optional) username to add to the operador group (will NOT mark as staff)",
        )

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="operador")

        # Ensure the group has no model-level permissions by clearing them.
        group.permissions.clear()

        self.stdout.write(self.style.SUCCESS(
            f"Group 'operador' {'created' if created else 'updated'} (no model permissions)."
        ))

        username = options.get("username")
        if username:
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User '{username}' does not exist."))
                return

            # Ensure operador users are not staff so they cannot access /admin/
            if user.is_staff:
                user.is_staff = False
                user.save()

            group.user_set.add(user)
            self.stdout.write(self.style.SUCCESS(f"User '{username}' assigned to 'operador' (not staff)."))

        self.stdout.write("")
        self.stdout.write("Note: 'operador' group members will not see Django admin unless you explicitly mark them staff.")
