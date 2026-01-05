import os

apps = {
    'catalog': 'Catalog',
    'customization': 'Customization',
    'orders': 'Orders',
    'gallery': 'Gallery',
    'reviews': 'Reviews',
    'pages': 'Pages',
    'seo': 'SEO',
    'core': 'Core'
}

base_dir = '/home/vasyl/Desktop/rest site/furniture_store/apps'

template = """from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class {class_name}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
    verbose_name = _('{verbose_name}')
"""

for app_name, verbose_name in apps.items():
    class_name = app_name.capitalize()
    content = template.format(class_name=class_name, app_name=app_name, verbose_name=verbose_name)
    file_path = os.path.join(base_dir, app_name, 'apps.py')
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Created {file_path}")
