from django.contrib import admin

# Register your models here.
from .models import *

#@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
	list_display = ['author','desc','create_date']
	list_filter = ('author','create_date')
admin.site.register(ImageModel, ImageModelAdmin)