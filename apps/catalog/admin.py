from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'show_on_home', 'order', 'created_at')
    list_filter = ('is_active', 'show_on_home')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'show_on_home', 'order')
    filter_horizontal = ('parents',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'is_customizable', 'is_active', 'show_on_home', 'updated_at')
    list_filter = ('categories', 'is_active', 'is_customizable', 'show_on_home')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('base_price', 'is_active', 'is_customizable', 'show_on_home')
    filter_horizontal = ('categories', 'available_materials')
