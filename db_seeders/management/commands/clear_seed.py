from django.core.management.base import BaseCommand
from django.db import transaction


from core.models import User
from flights.models import Address, Airport, Booking, Currency, Customer, Flight, Payment, Promotion


class Command(BaseCommand):
    help = "Clear seeded data from the database"

    def add_arguments(self, parser):
        parser.add_argument('--users', action='store_true', help="Clear users")
        parser.add_argument('--promotions', action='store_true', help="Clear promotions")
        parser.add_argument('--customers', action='store_true', help="Clear customers")
        parser.add_argument('--currencies', action='store_true', help="Clear currencies")
        parser.add_argument('--flights', action='store_true', help="Clear flights")
        parser.add_argument('--addresses', action='store_true', help="Clear addresses")
        parser.add_argument('--airports', action='store_true', help="Clear airports")
        parser.add_argument('--bookings', action='store_true', help="Clear bookings")
        parser.add_argument('--payments', action='store_true', help="Clear payments")
        parser.add_argument('--all', action='store_true', help="Clear everything")

    @transaction.atomic
    def handle(self, *args, **options):
        if options['all'] or options['promotions']:
            Promotion.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All promotions are deleted"))
            
        if options['all'] or options['currencies']:
            Currency.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All currencies are deleted"))
            
        if options['all'] or options['flights']:
            Flight.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All flights are deleted"))
            
        if options['all'] or options['airports']:
            Airport.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All airports are deleted"))
            
        if options['all'] or options['addresses']:
            Address.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All addresses are deleted"))
        
        if options['all'] or options['customers']:
            Customer.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All customers are deleted"))
        
        if options['all'] or options['bookings']:
            Booking.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All bookings are deleted"))
            
        if options['all'] or options['payments']:
            Payment.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All payments are deleted"))

        if options['all'] or options['users']:
            User.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All users deleted"))

        if not options['users'] and not options['promotions'] and not options['all']:
            self.stdout.write(self.style.WARNING("No option specified. Use --users, --promotions, or --all"))
