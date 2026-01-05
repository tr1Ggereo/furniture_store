from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel
from apps.catalog.models import Product

class OrderRequest(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = 'new', _('New')
        CONTACTED = 'contacted', _('Contacted')
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')

    name = models.CharField(_("Name"), max_length=100)
    phone = models.CharField(_("Phone"), max_length=20)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Product"))
    project = models.ForeignKey('gallery.Project', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Project"))
    material = models.ManyToManyField('customization.Material', blank=True, verbose_name=_("Selected Materials"))
    pattern = models.ForeignKey('customization.Pattern', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Pattern"))
    
    width = models.PositiveIntegerField(_("Width (mm)"), null=True, blank=True)
    height = models.PositiveIntegerField(_("Height (mm)"), null=True, blank=True)
    depth = models.PositiveIntegerField(_("Depth (mm)"), null=True, blank=True)
    
    message = models.TextField(_("Message"), blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.NEW)

    class Meta:
        verbose_name = _("Order Request")
        verbose_name_plural = _("Order Requests")

    def __str__(self):
        return f"Order from {self.name}"
