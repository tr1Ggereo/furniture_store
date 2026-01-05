from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import OrderRequest

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class DashboardView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = OrderRequest
    template_name = 'crm/dashboard.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        search = self.request.GET.get('q')
        
        if status:
            queryset = queryset.filter(status=status)
        if search:
            queryset = queryset.filter(phone__icontains=search)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Status breakdown
        stats = OrderRequest.objects.values('status').annotate(total=Count('id'))
        stats_dict = {s['status']: s['total'] for s in stats}
        
        context['total_count'] = OrderRequest.objects.count()
        context['new_count'] = stats_dict.get(OrderRequest.Status.NEW, 0)
        context['processed_count'] = sum(
            stats_dict.get(status, 0) for status in [
                OrderRequest.Status.CONTACTED,
                OrderRequest.Status.IN_PROGRESS,
                OrderRequest.Status.COMPLETED
            ]
        )
        
        # Daily stats for the last 14 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=13)
        
        daily_stats = OrderRequest.objects.filter(
            created_at__date__range=[start_date, end_date]
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        # Prepare data for Chart.js
        daily_data = {s['date']: s['count'] for s in daily_stats}
        chart_labels = []
        chart_data = []
        
        for i in range(14):
            day = start_date + timedelta(days=i)
            chart_labels.append(day.strftime('%d.%m'))
            chart_data.append(daily_data.get(day, 0))
            
        context['chart_labels'] = chart_labels
        context['chart_data'] = chart_data
        
        context['status_choices'] = OrderRequest.Status.choices
        context['current_status'] = self.request.GET.get('status', '')
        return context

class OrderDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = OrderRequest
    template_name = 'crm/order_detail.html'
    context_object_name = 'order'

class OrderStatusUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = OrderRequest
    fields = ['status']
    success_url = reverse_lazy('crm:dashboard')

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.POST.get('status')
        if new_status in dict(OrderRequest.Status.choices):
            order.status = new_status
            order.save()
        return redirect('crm:dashboard')

class OrderDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = OrderRequest
    success_url = reverse_lazy('crm:dashboard')
    template_name = 'crm/order_confirm_delete.html'
