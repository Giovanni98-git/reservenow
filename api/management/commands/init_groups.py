from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Groupes initialization: Admin, Manager, Client"

    def handle(self, *args, **options):
        # === Groupe Admin ===
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        self.stdout.write(self.style.SUCCESS("✔ Admin group created (all permissions by default)"))

        # === Groupe Manager ===
        manager_group, created = Group.objects.get_or_create(name="Manager")
        if created:
            manager_group.permissions.set(Permission.objects.all())
            self.stdout.write(self.style.SUCCESS("✔ Manager group created with all permissions"))
        else:
            self.stdout.write(self.style.WARNING("⚠ Manager group already exists"))

        # === Groupe Client ===
        client_group, created = Group.objects.get_or_create(name="Client")
        if created:
            perms = Permission.objects.filter(
                codename__in=[
                    "view_menu",
                    "add_reservation",
                    "change_reservation",
                    "delete_reservation",
                    "view_tablesaloon",
                    "view_schedule",
                ]
            )
            client_group.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS("✔ Client group created with limited permissions"))
        else:
            self.stdout.write(self.style.WARNING("⚠ Client group already exists"))

        self.stdout.write(self.style.SUCCESS("✔ Group initialization complete"))
