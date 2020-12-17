from django.contrib import admin
from .models import PakAdm3
from leaflet.admin import LeafletGeoAdmin
# Register your models here.

admin.site.register(PakAdm3,LeafletGeoAdmin)