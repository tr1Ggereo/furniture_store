from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel

class Project(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    main_image = models.ImageField(_("Main Image"), upload_to='gallery/main/')
    is_featured = models.BooleanField(_("Featured"), default=False)
    is_published = models.BooleanField(_("Published"), default=True)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.title

class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name=_("Project"))
    image = models.ImageField(_("Image"), upload_to='gallery/projects/')
    caption = models.CharField(_("Caption"), max_length=200, blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Project Image")
        verbose_name_plural = _("Project Images")
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.project.title}"
