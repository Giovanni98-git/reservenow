import json
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models.menus import Menu

class Command(BaseCommand):
    help = "Initialize the Menu table with data from burgers.json"

    def add_arguments(self, parser):
        parser.add_argument('--json-file', default='burgers.json', help='Path to the JSON file (default: burgers.json)')
        parser.add_argument('--user-email', default='admin@example.com', help='Email of the user to associate with menu items')

    def handle(self, *args, **options):
        json_file = options['json_file']
        user_email = options['user_email']
        User = get_user_model()

        # Vérifier si l'utilisateur existe
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"⚠ Erreur : L'utilisateur '{user_email}' n'existe pas. Exécutez 'init_users' d'abord."))
            return

        # Vérifier si le fichier JSON existe
        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(f"⚠ Erreur : Le fichier '{json_file}' n'existe pas."))
            return

        # Lire le fichier JSON
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"⚠ Erreur : Le fichier '{json_file}' n'est pas un JSON valide."))
            return

        # Initialiser les entrées du menu
        for item in data:
            try:
                Menu.objects.create_from_json(item, user)
                self.stdout.write(self.style.SUCCESS(f"✔ Menu '{item['name']}' créé avec succès"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠ Menu '{item['name']}' non créé : {str(e)}"))

        self.stdout.write(self.style.SUCCESS("✔ Initialisation du menu terminée"))