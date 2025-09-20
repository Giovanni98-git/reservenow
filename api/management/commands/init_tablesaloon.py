import json
import os
from django.core.management.base import BaseCommand
from api.models.tableSaloons import TableSaloon

class Command(BaseCommand):
    help = "Initialize the TableSaloon table with data from tablesaloon.json"

    def add_arguments(self, parser):
        parser.add_argument('--json-file', default='tablesaloon.json', help='Path to the JSON file (default: tablesaloon.json)')

    def handle(self, *args, **options):
        json_file = options['json_file']

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

        # Initialiser les entrées TableSaloon
        for item in data:
            try:
                TableSaloon.objects.create(
                    name=item['name'],
                    capacity=item['capacity'],
                    type=item['type'],
                    status=item['status'],
                    img=item.get('img', '')  # img peut être vide si non fourni
                )
                self.stdout.write(self.style.SUCCESS(f"✔ Table/Saloon '{item['name']}' créé avec succès"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠ Table/Saloon '{item['name']}' non créé : {str(e)}"))

        self.stdout.write(self.style.SUCCESS("✔ Initialisation de TableSaloon terminée"))