from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CustomizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.customization'
    verbose_name = _('Customization')
