from django.contrib import admin
from django.apps import apps

# Get all models from your project
models = apps.get_models()


# Custom admin class with enhanced functionality
class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        self.list_filter = [field.name for field in model._meta.fields if
                            field.get_internal_type() in ['BooleanField', 'DateField', 'DateTimeField', 'ForeignKey',
                                                          'ManyToManyField']]
        self.search_fields = [field.name for field in model._meta.fields if
                              field.get_internal_type() not in ['BooleanField', 'DateField', 'DateTimeField']]
        super(CustomModelAdmin, self).__init__(model, admin_site)


# Register all models with the custom admin class
for model in models:
    try:
        admin.site.register(model, CustomModelAdmin)
    except admin.sites.AlreadyRegistered:
        pass
