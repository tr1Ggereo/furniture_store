from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order_status_update'),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_confirm_delete'),
]
