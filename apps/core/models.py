from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True

class HomeSettings(TimeStampedModel):
    hero_title = models.CharField(_("Hero Title"), max_length=200, default="Меблі вашої мрії в Івано-Франківську")
    hero_subtitle = models.TextField(_("Hero Subtitle"), blank=True, default="Індивідуальний підхід до кожного клієнта. Створюйте затишок разом з нами.")
    hero_image = models.ImageField(_("Hero Background Image"), upload_to='home/', blank=True, null=True)
    
    custom_section_image = models.ImageField(_("Custom Section Image"), upload_to='home/', blank=True, null=True)
    why_us_image = models.ImageField(_("Why Us Section Image"), upload_to='home/', blank=True, null=True)
    
    contact_phone = models.CharField(_("Contact Phone"), max_length=20, default="+38 (0XX) XXX-XX-XX")
    contact_email = models.EmailField(_("Contact Email"), blank=True)
    address = models.CharField(_("Address"), max_length=255, default="м. Івано-Франківськ, вул. ...")
    working_hours = models.CharField(_("Working Hours"), max_length=100, default="Пн-Пт: 9:00 - 18:00")
    
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    class Meta:
        verbose_name = _("Home Settings")
        verbose_name_plural = _("Home Settings")

    def __str__(self):
        return str(_("Home Page Settings"))

    def save(self, *args, **kwargs):
        if not self.pk and HomeSettings.objects.exists():
            return
        super().save(*args, **kwargs)
