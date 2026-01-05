from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.cache import cache
from django.contrib import messages
from .models import OrderRequest

from .forms import OrderForm

class OrderCreateView(CreateView):
    model = OrderRequest
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('core:home')

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_initial(self):
        initial = super().get_initial()
        product_id = self.request.GET.get('product')
        project_id = self.request.GET.get('project')
        material_ids = self.request.GET.getlist('material')
        if product_id:
            initial['product'] = product_id
        if project_id:
            initial['project'] = project_id
        if material_ids:
            initial['material'] = material_ids
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Determine if this is a product-specific order, project consultation, or general consultation
        product_id = self.request.GET.get('product')
        project_id = self.request.GET.get('project')
        is_customizing = self.request.GET.get('customize') == 'true'
        
        context['is_product_order'] = bool(product_id)
        context['is_project_consultation'] = bool(project_id)
        context['is_customizing'] = is_customizing
        
        if product_id:
            try:
                from apps.catalog.models import Product
                product_obj = Product.objects.get(id=product_id)
                context['product_name_from_get'] = product_obj.name
                context['available_materials'] = product_obj.available_materials.filter(is_active=True)
            except (Product.DoesNotExist, ValueError):
                pass
        else:
            from apps.customization.models import Material
            context['available_materials'] = Material.objects.filter(is_active=True)
                
        if project_id:
            try:
                from apps.gallery.models import Project
                context['project_name_from_get'] = Project.objects.get(id=project_id).title
            except (Project.DoesNotExist, ValueError):
                pass
                
        from apps.customization.models import Pattern
        context['all_patterns'] = Pattern.objects.filter(is_active=True)

        # Pre-calculate selections for template to avoid complex tags
        form = context.get('form')
        selected_mats = []
        selected_pat = None

        if form:
            val = form['material'].value()
            if val:
                if isinstance(val, (list, tuple)):
                    selected_mats = [str(v) for v in val]
                else:
                    selected_mats = [str(val)]
            
            p_val = form['pattern'].value()
            if p_val:
                selected_pat = str(p_val)

        context['selected_material_ids'] = selected_mats
        context['selected_pattern_id'] = selected_pat
        
        return context

    def form_valid(self, form):
        ip = self.get_client_ip()
        cache_key = f"order_limit_{ip}"
        
        if cache.get(cache_key):
            messages.error(self.request, "Спробуйте через 15 хвилин, ви вже подавали заявку")
            return self.form_invalid(form)
            
        # Set cache for 15 minutes (900 seconds)
        cache.set(cache_key, True, 900)
        
        messages.success(self.request, "Дякуємо! Ваша заявка прийнята. Ми зв'яжемося з вами найближчим часом.")
        return super().form_valid(form)
