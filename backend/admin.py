from django.contrib import admin
from . import models
from django.contrib.admin import AdminSite

for model_name in dir(models):
    model = getattr(models, model_name)
    if hasattr(model, '_meta') and not model._meta.abstract:
        admin.site.register(model)

class CustomAdminSite(AdminSite):
    site_header = models.Company.objects.first().name