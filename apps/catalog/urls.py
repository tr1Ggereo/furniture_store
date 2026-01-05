from django.urls import path
from .views import CategoryListView, CategoryDetailView, ProductDetailView

app_name = 'catalog'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
