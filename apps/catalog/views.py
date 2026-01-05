from django.views.generic import ListView, DetailView
from .models import Category, Product

class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        # Only show root categories (those without parents)
        return Category.objects.filter(is_active=True, parents__isnull=True)

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'catalog/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get children categories
        context['subcategories'] = self.object.children.filter(is_active=True)
        # Get products in this category
        context['products'] = self.object.products.filter(is_active=True)
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related products (sharing same categories)
        context['related_products'] = Product.objects.filter(
            categories__in=self.object.categories.all(),
            is_active=True
        ).exclude(id=self.object.id).distinct()[:4]
        return context
