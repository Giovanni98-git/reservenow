from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command

class Command(BaseCommand):
    help = "Initialize three users: a superuser, a Manager, and a Client"

    def add_arguments(self, parser):
        # Arguments pour le superutilisateur (first_name et last_name requis)
        parser.add_argument('--superuser-email', default='admin@example.com', help='Email for superuser')
        parser.add_argument('--superuser-password', default='admin123', help='Password for superuser')
        parser.add_argument('--superuser-first-name', default='Admin', help='First name for superuser')
        parser.add_argument('--superuser-last-name', default='User', help='Last name for superuser')

        # Arguments pour le Manager (first_name et last_name optionnels)
        parser.add_argument('--manager-email', default='manager@example.com', help='Email for Manager')
        parser.add_argument('--manager-password', default='manager123', help='Password for Manager')
        parser.add_argument('--manager-first-name', default='', help='First name for Manager')
        parser.add_argument('--manager-last-name', default='', help='Last name for Manager')

        # Arguments pour le Client (first_name et last_name optionnels)
        parser.add_argument('--client-email', default='client@example.com', help='Email for Client')
        parser.add_argument('--client-password', default='client123', help='Password for Client')
        parser.add_argument('--client-first-name', default='', help='First name for Client')
        parser.add_argument('--client-last-name', default='', help='Last name for Client')

    def handle(self, *args, **options):
        User = get_user_model()

        # Exécuter les migrations pour s'assurer que les groupes et permissions existent
        self.stdout.write(self.style.NOTICE("Exécution des migrations..."))
        call_command('migrate')

        # Vérifier que les groupes Manager et Client existent
        try:
            manager_group = Group.objects.get(name="Manager")
            client_group = Group.objects.get(name="Client")
        except Group.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f"⚠ Erreur : Groupe manquant ({str(e)}). Assurez-vous que le signal post_migrate est configuré."))
            return

        # Créer le superutilisateur
        superuser_email = options['superuser_email']
        superuser_password = options['superuser_password']
        superuser_first_name = options['superuser_first_name']
        superuser_last_name = options['superuser_last_name']
        if not User.objects.filter(email=superuser_email).exists():
            User.objects.create_superuser(
                email=superuser_email,
                password=superuser_password,
                first_name=superuser_first_name,
                last_name=superuser_last_name
            )
            self.stdout.write(self.style.SUCCESS(f"✔ Superuser '{superuser_email}' créé"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠ Superuser '{superuser_email}' existe déjà"))

        # Créer l'utilisateur Manager
        manager_email = options['manager_email']
        manager_password = options['manager_password']
        manager_first_name = options['manager_first_name']
        manager_last_name = options['manager_last_name']
        if not User.objects.filter(email=manager_email).exists():
            manager_user = User.objects.create_user(
                email=manager_email,
                password=manager_password,
                first_name=manager_first_name,
                last_name=manager_last_name
            )
            manager_user.groups.add(manager_group)
            self.stdout.write(self.style.SUCCESS(f"✔ Utilisateur Manager '{manager_email}' créé et ajouté au groupe Manager"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠ Utilisateur Manager '{manager_email}' existe déjà"))

        # Créer l'utilisateur Client
        client_email = options['client_email']
        client_password = options['client_password']
        client_first_name = options['client_first_name']
        client_last_name = options['client_last_name']
        if not User.objects.filter(email=client_email).exists():
            client_user = User.objects.create_user(
                email=client_email,
                password=client_password,
                first_name=client_first_name,
                last_name=client_last_name
            )
            client_user.groups.add(client_group)
            self.stdout.write(self.style.SUCCESS(f"✔ Utilisateur Client '{client_email}' créé et ajouté au groupe Client"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠ Utilisateur Client '{client_email}' existe déjà"))

        self.stdout.write(self.style.SUCCESS("✔ Initialisation des utilisateurs terminée"))