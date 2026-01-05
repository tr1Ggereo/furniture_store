from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel
from apps.catalog.models import Product

class Pattern(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)
    image = models.ImageField(_("Pattern Image"), upload_to='patterns/')
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        verbose_name = _("Pattern")
        verbose_name_plural = _("Patterns")

    def __str__(self):
        return self.name

class Material(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)
    image = models.ImageField(_("Image"), upload_to='materials/', blank=True, null=True)
    description = models.TextField(_("Short Description"), blank=True)
    price_multiplier = models.DecimalField(_("Price Multiplier"), max_digits=4, decimal_places=2, default=1.0)
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")

    def __str__(self):
        return self.name

class CustomizationRequest(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = 'new', _('New')
        CONTACTED = 'contacted', _('Contacted')
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    pattern = models.ForeignKey(Pattern, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Pattern"))
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Material"))
    
    width = models.PositiveIntegerField(_("Width (mm)"), null=True, blank=True)
    height = models.PositiveIntegerField(_("Height (mm)"), null=True, blank=True)
    depth = models.PositiveIntegerField(_("Depth (mm)"), null=True, blank=True)
    
    customer_name = models.CharField(_("Customer Name"), max_length=100)
    phone = models.CharField(_("Phone"), max_length=20)
    comment = models.TextField(_("Comment"), blank=True)
    
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.NEW)

    class Meta:
        verbose_name = _("Customization Request")
        verbose_name_plural = _("Customization Requests")

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"
