from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Contact)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

# admin.site.register(models.Contact)

