from django.contrib.gis.db import models
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
# Create your models here.
class PakAdm3(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    id_0 = models.BigIntegerField(blank=True, null=True)
    iso = models.CharField(max_length=3, blank=True, null=True)
    name_0 = models.CharField(max_length=75, blank=True, null=True)
    id_1 = models.BigIntegerField(blank=True, null=True)
    name_1 = models.CharField(max_length=75, blank=True, null=True)
    id_2 = models.BigIntegerField(blank=True, null=True)
    name_2 = models.CharField(max_length=75, blank=True, null=True)
    id_3 = models.BigIntegerField(blank=True, null=True)
    name_3 = models.CharField(max_length=75, blank=True, null=True)
    type_3 = models.CharField(max_length=50, blank=True, null=True)
    engtype_3 = models.CharField(max_length=50, blank=True, null=True)
    nl_name_3 = models.CharField(max_length=75, blank=True, null=True)
    varname_3 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PAK_adm3'
    def __str__(self):
        return self.name_3

class ThreatValue(models.Model):
    ID = models.IntegerField
    name=models.CharField(max_length=75)
    model=models.CharField(max_length=75)

    typ=models.CharField(max_length=75)
    def __str__(self):
        return self.name 
class WeaponLoc(models.Model):
    lat= models.DecimalField(max_digits=22,decimal_places=16)
    lon= models.DecimalField(max_digits=22,decimal_places=16)
    name= models.CharField(max_length=50, blank=True, null=True)

class DefendedAssetLoc(models.Model):
    lat= models.DecimalField(max_digits=22,decimal_places=16)
    lon= models.DecimalField(max_digits=22,decimal_places=16)
    name= models.CharField(max_length=50, blank=True, null=True)
    vitality=models.IntegerField(null=True)

class SimulatorEssential(models.Model):
    simulationTime=models.IntegerField(default=10)
    numberOfThreats=models.IntegerField(default=4)

class SimulatorEssentialAdmin(admin.ModelAdmin):
    def has_add_permission(self, *args, **kwargs):
        return not SimulatorEssential.objects.exists()