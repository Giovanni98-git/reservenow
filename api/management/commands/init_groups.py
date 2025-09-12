from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from api.models import Menu, Reservation, TableSaloon, Schedule  # Ajoutez vos modèles

class Command(BaseCommand):
    help = "Groupes initialization: Admin, Manager, Client"

    def handle(self, *args, **options):
        User = get_user_model()

        # === Groupe Admin ===
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        self.stdout.write(self.style.SUCCESS("✔ Admin group created (all permissions by default)"))

        # === Groupe Manager ===
        manager_group, created = Group.objects.get_or_create(name="Manager")
        if created:
            try:
                manager_group.permissions.set(Permission.objects.all())
                self.stdout.write(self.style.SUCCESS("✔ Manager group created with all permissions"))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR("⚠ Erreur : Certaines permissions sont manquantes. Vérifiez les migrations."))
        else:
            self.stdout.write(self.style.WARNING("⚠ Manager group already exists"))

        # === Groupe Client ===
        client_group, created = Group.objects.get_or_create(name="Client")
        if created:
            try:
                # Obtenir les content types pour chaque modèle
                content_types = {
                    'menu': ContentType.objects.get_for_model(Menu),
                    'reservation': ContentType.objects.get_for_model(Reservation),
                    'tablesaloon': ContentType.objects.get_for_model(TableSaloon),
                    'schedule': ContentType.objects.get_for_model(Schedule),
                }
                perms = Permission.objects.filter(
                    content_type__in=content_types.values(),
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
            except (ContentType.DoesNotExist, Permission.DoesNotExist):
                self.stdout.write(self.style.ERROR("⚠ Erreur : Certains modèles ou permissions sont manquants. Vérifiez les migrations."))
        else:
            self.stdout.write(self.style.WARNING("⚠ Client group already exists"))

        self.stdout.write(self.style.SUCCESS("✔ Group initialization complete"))