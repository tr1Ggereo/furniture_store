from django.contrib import admin
from .models import OrderRequest

@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'product', 'project', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'message')
    filter_horizontal = ('material',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('status', 'name', 'phone')
        }),
        ('Context', {
            'fields': ('product', 'project', 'material')
        }),
        ('Customization / Dimensions', {
            'fields': ('pattern', 'width', 'height', 'depth'),
            'description': 'Dimensions and pattern for custom orders'
        }),
        ('Additional Info', {
            'fields': ('message', 'created_at')
        }),
    )
