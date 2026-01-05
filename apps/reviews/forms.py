from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'text', 'rating']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} ★") for i in range(5, 0, -1)]),
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ваш відгук...'}),
            'name': forms.TextInput(attrs={'placeholder': "Ваше ім'я..."}),
        }
