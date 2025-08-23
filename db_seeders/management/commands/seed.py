from typing import Any
from django.core.management.base import BaseCommand

from db_seeders.seeders import core_app_seeder, flights_app_seeder


class Command(BaseCommand):
    help = 'Seed the database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('--flights', type=int, default=200, help="Number of data generated for flights app")
        parser.add_argument('--core', type=int, default=200, help="Number of data generated for core app")
    
    def handle(self, *args:Any, **options:Any):
        self.stdout.write(self.style.SUCCESS('Seeding the database...'))
        
        # core_app_seeder.run(data=options['core'])
        flights_app_seeder.run(data=options['flights'])

        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

