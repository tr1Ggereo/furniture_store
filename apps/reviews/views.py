from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Review
from .forms import ReviewForm

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        messages.success(self.request, "Дякуємо! Ваш відгук надіслано на модерацію.")
        return super().form_valid(form)
