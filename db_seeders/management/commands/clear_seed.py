# core/management/commands/clear_seed.py
from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import User
from posts.models import Post

class Command(BaseCommand):
    help = "Clear seeded data from the database"

    def add_arguments(self, parser):
        parser.add_argument('--users', action='store_true', help="Clear users")
        parser.add_argument('--posts', action='store_true', help="Clear posts")
        parser.add_argument('--all', action='store_true', help="Clear everything")

    @transaction.atomic
    def handle(self, *args, **options):
        if options['all'] or options['posts']:
            Post.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All posts deleted"))

        if options['all'] or options['users']:
            User.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All users deleted"))

        if not options['users'] and not options['posts'] and not options['all']:
            self.stdout.write(self.style.WARNING("No option specified. Use --users, --posts, or --all"))
