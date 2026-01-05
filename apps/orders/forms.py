from django import forms
from .models import OrderRequest
from apps.customization.models import Material

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = ['name', 'phone', 'product', 'project', 'pattern', 'width', 'height', 'depth', 'material', 'message']
        widgets = {
            'material': forms.CheckboxSelectMultiple(),
            'pattern': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If no product or project is selected (general consultation), hide material selection
        project_id = None
        if self.data and self.data.get('project'):
            project_id = self.data.get('project')
        elif self.initial and self.initial.get('project'):
            project_id = self.initial.get('project')

        product_id = None
        if self.data and self.data.get('product'):
            product_id = self.data.get('product')
        elif self.initial and self.initial.get('product'):
            product_id = self.initial.get('product')

        if not product_id and not project_id:
            self.fields['material'].widget = forms.HiddenInput()
            self.fields['material'].required = False
            self.fields['product'].widget = forms.HiddenInput()
            self.fields['product'].required = False
            self.fields['project'].widget = forms.HiddenInput()
            self.fields['project'].required = False
        elif project_id:
            # If a project is selected
            self.fields['material'].widget = forms.HiddenInput()
            self.fields['material'].required = False
            self.fields['product'].widget = forms.HiddenInput()
            self.fields['product'].required = False
            self.fields['project'].widget = forms.HiddenInput()
        else:
            # If product is selected
            self.fields['project'].widget = forms.HiddenInput()
            self.fields['project'].required = False
            try:
                from apps.catalog.models import Product
                product_obj = Product.objects.get(id=product_id)
                self.fields['material'].queryset = product_obj.available_materials.all()
                # Make product field readonly/hidden if it's already selected
                self.fields['product'].widget = forms.HiddenInput()
            except (Product.DoesNotExist, ValueError, TypeError):
                self.fields['material'].widget = forms.HiddenInput()
                self.fields['material'].required = False
                self.fields['product'].widget = forms.HiddenInput()
                self.fields['product'].required = False
        
        # Ensure message is optional
        self.fields['message'].required = False

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Ім'я не може містити цифри.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        # Extract digits to check length
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) < 9:
            raise forms.ValidationError("Номер телефону повинен містити мінімум 9 цифр.")
        return phone
