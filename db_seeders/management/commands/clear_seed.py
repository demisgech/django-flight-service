from django.core.management.base import BaseCommand
from django.db import transaction


from core.models import User
from flights.models import Promotion


class Command(BaseCommand):
    help = "Clear seeded data from the database"

    def add_arguments(self, parser):
        parser.add_argument('--users', action='store_true', help="Clear users")
        parser.add_argument('--promotions', action='store_true', help="Clear promotions")
        parser.add_argument('--all', action='store_true', help="Clear everything")

    @transaction.atomic
    def handle(self, *args, **options):
        if options['all'] or options['promotions']:
            Promotion.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All promotions deleted"))

        if options['all'] or options['users']:
            User.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All users deleted"))

        if not options['users'] and not options['promotions'] and not options['all']:
            self.stdout.write(self.style.WARNING("No option specified. Use --users, --promotions, or --all"))
