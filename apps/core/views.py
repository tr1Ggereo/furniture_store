from django.views.generic import TemplateView
from apps.core.models import HomeSettings
from apps.catalog.models import Product, Category
from apps.gallery.models import Project
from apps.reviews.models import Review

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch configurations (get first or create empty)
        home_settings = HomeSettings.objects.first()
        if not home_settings:
            home_settings = HomeSettings()
            
        context['settings'] = home_settings
        context['home_products'] = Product.objects.filter(is_active=True, show_on_home=True)[:6]
        context['home_categories'] = Category.objects.filter(is_active=True, show_on_home=True).order_by('order')[:6]
        context['featured_projects'] = Project.objects.filter(is_published=True, is_featured=True)[:4]
        context['reviews'] = Review.objects.filter(is_published=True)[:5]
        return context
