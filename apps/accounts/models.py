from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel

class User(AbstractUser, TimeStampedModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        MANAGER = 'manager', _('Manager')
        CUSTOMER = 'customer', _('Customer')

    phone = models.CharField(_("Phone number"), max_length=20, blank=True)
    role = models.CharField(_("Role"), max_length=10, choices=Role.choices, default=Role.CUSTOMER)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username
