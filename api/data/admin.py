from django.contrib import admin
from .models import ThreatInitial
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(ThreatInitial)
class WeaponAdmin(ImportExportModelAdmin):
    pass
