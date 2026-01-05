from django.contrib import admin
from .models import Pattern, Material, CustomizationRequest

@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_multiplier', 'is_active', 'created_at')
    list_editable = ('price_multiplier', 'is_active')
    search_fields = ('name', 'description')

@admin.register(CustomizationRequest)
class CustomizationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'product', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone', 'product__name')
    readonly_fields = ('created_at', 'updated_at')
