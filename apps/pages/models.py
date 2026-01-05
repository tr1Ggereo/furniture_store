from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel

from ckeditor.fields import RichTextField

class Page(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    content = RichTextField(_("Content"), blank=True)
    
    # SEO Fields
    seo_title = models.CharField(_("SEO Title"), max_length=200, blank=True)
    seo_description = models.TextField(_("SEO Description"), blank=True)

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
