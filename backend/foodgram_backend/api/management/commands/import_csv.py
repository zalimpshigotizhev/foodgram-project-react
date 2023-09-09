import csv
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import CSV data into MyModel'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(Ingredient.objects.filter(name=row[0])) == 0:
                    ingredient = Ingredient()
                    ingredient.name = row[0]
                    ingredient.measurement_unit = row[1]
                    ingredient.save()
