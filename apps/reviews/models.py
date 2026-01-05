from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel

class Review(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)
    text = models.TextField(_("Review Text"))
    rating = models.PositiveSmallIntegerField(_("Rating"), default=5, choices=[(i, str(i)) for i in range(1, 6)])
    is_published = models.BooleanField(_("Is Published"), default=False)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating}"
