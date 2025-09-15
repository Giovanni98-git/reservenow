from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from api.models import Menu, Reservation, TableSaloon, Schedule

class Command(BaseCommand):
    help = "Groupes initialization: Manager, Client"

    def handle(self, *args, **options):
        # Exécuter les migrations pour s'assurer que les ContentType et permissions existent
        self.stdout.write(self.style.NOTICE("Exécution des migrations..."))
        call_command('migrate')

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
            except (ContentType.DoesNotExist, Permission.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f"⚠ Erreur : {str(e)}. Vérifiez les migrations et les modèles."))
        else:
            self.stdout.write(self.style.WARNING("⚠ Client group already exists"))

        self.stdout.write(self.style.SUCCESS("✔ Group initialization complete"))