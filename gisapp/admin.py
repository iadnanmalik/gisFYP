from django.contrib import admin
from .models import PakAdm3,SimulatorEssential,SimulatorEssentialAdmin
from .models import ThreatValue,WeaponLoc,DefendedAssetLoc
from leaflet.admin import LeafletGeoAdmin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(WeaponLoc,DefendedAssetLoc)
class WeaponAdmin(ImportExportModelAdmin):
    pass

# Register your models here.

admin.site.register(PakAdm3,LeafletGeoAdmin)
admin.site.register(ThreatValue)
admin.site.register(SimulatorEssential,SimulatorEssentialAdmin)
