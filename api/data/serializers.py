from rest_framework import serializers
from .models import ThreatInitial


class ThreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatInitial
        fields = ['lat', 'lon', 'angle'] 