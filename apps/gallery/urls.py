from django.urls import path
from .views import GalleryListView, ProjectDetailView

app_name = 'gallery'

urlpatterns = [
    path('', GalleryListView.as_view(), name='project_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
]
