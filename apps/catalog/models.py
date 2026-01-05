from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel

class Category(TimeStampedModel):
    parents = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='children', 
        blank=True, 
        verbose_name=_("Parent Categories")
    )
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    image = models.ImageField(_("Image"), upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(_("Is active"), default=True)
    show_on_home = models.BooleanField(_("Show on Home Page"), default=False)
    order = models.PositiveIntegerField(_("Display Order"), default=0)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

from ckeditor.fields import RichTextField

class Product(TimeStampedModel):
    categories = models.ManyToManyField(
        Category, 
        related_name='products', 
        verbose_name=_("Categories")
    )
    name = models.CharField(_("Name"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    base_price = models.DecimalField(_("Base price"), max_digits=10, decimal_places=2)
    description = RichTextField(_("Description"), blank=True)
    image = models.ImageField(_("Image"), upload_to='products/', blank=True, null=True)
    available_materials = models.ManyToManyField(
        'customization.Material', 
        related_name='products', 
        blank=True, 
        verbose_name=_("Available Materials")
    )
    is_customizable = models.BooleanField(_("Is customizable"), default=True)
    is_active = models.BooleanField(_("Is active"), default=True)
    show_on_home = models.BooleanField(_("Show on Home Page"), default=False)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
