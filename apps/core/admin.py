from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import HomeSettings

@admin.register(HomeSettings)
class HomeSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Hero Section'), {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image')
        }),
        (_('Custom Section'), {
            'fields': ('custom_section_image',)
        }),
        (_('Why Us Section'), {
            'fields': ('why_us_image',)
        }),
        (_('Contacts'), {
            'fields': ('contact_phone', 'contact_email', 'address', 'working_hours')
        }),
        (_('Social'), {
            'fields': ('facebook_url', 'instagram_url')
        }),
    )

    def has_add_permission(self, request):
        if HomeSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False
