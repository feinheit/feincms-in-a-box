from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<password>'
    help = 'Updates all empty passwords to the given password'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Pass the password')

        for user in get_user_model()._default_manager.filter(password=''):
            user.set_password(args[0])
            user.save()
