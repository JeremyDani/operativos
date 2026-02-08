from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = (
        "Create or update the 'administrador' group with permissions limited to "
        "the 'auth' and 'cuenta' apps. Optionally assign a username to the group "
        "and mark the user as staff so they can access /admin/."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--user",
            dest="username",
            help="(optional) username to add to the administrador group and mark as staff",
        )

    def handle(self, *args, **options):
        app_labels = ["auth", "cuenta"]

        group, created = Group.objects.get_or_create(name="administrador")

        # Clear existing permissions and assign only permissions for the specified apps
        group.permissions.clear()
        perms = Permission.objects.filter(content_type__app_label__in=app_labels)
        group.permissions.set(perms)

        self.stdout.write(self.style.SUCCESS(
            f"Group 'administrador' {'created' if created else 'updated'} with {perms.count()} permissions."
        ))

        username = options.get("username")
        if username:
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User '{username}' does not exist."))
                return

            # Make sure the user can access the admin
            if not user.is_staff:
                user.is_staff = True
                user.save()

            group.user_set.add(user)
            self.stdout.write(self.style.SUCCESS(f"User '{username}' assigned to 'administrador' and marked as staff."))

        self.stdout.write("")
        self.stdout.write("Next steps:")
        self.stdout.write(" - Log into /admin/ with a user assigned to the 'administrador' group.")
        self.stdout.write(" - The admin interface will only show models for which the group has permissions (auth and cuenta).")
