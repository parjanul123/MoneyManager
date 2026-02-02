from django.core.management.commands.runserver import Command as RunServerCommand

class Command(RunServerCommand):
    """Custom runserver command că pornește pe 127.0.0.1:9512"""
    
    def add_arguments(self, parser):
        super().add_arguments(parser)
        # Setează default-ul
        parser.set_defaults(addrport='127.0.0.1:9512')

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                '\n' + '='*60
                + '\n🚀 Money Manager Server'
                + '\n📍 http://127.0.0.1:9512/'
                + '\n' + '='*60 + '\n'
            )
        )
        return super().handle(*args, **options)
