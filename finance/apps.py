from django.apps import AppConfig


class FinanceConfig(AppConfig):
    name = 'finance'
    
    def ready(self):
        # Importă semnalele pentru sincronizarea datelor de Discord
        import finance.signals
