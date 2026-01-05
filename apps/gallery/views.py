from django.views.generic import ListView, DetailView
from .models import Project

class GalleryListView(ListView):
    model = Project
    template_name = 'gallery/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(is_published=True)

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'gallery/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        return context
