from django.db import models

# Create your models here.
class ThreatInitial(models.Model):
    lat= models.DecimalField(max_digits=22,decimal_places=16)
    lon= models.DecimalField(max_digits=22,decimal_places=16)
    angle = models.IntegerField(default=0,null=True)
  