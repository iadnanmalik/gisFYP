from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import ThreatInitial
from .serializers import ThreatSerializer
import random


@csrf_exempt
def get_threats(request):
    """
    List all code snippets, or create a new snippet.
    """
    threats = ThreatInitial.objects.all()
    if request.method == 'GET':
        serializer = ThreatSerializer(threats, many=True)
        data= serializer.data[random.randint(0,len(serializer.data))]
        return JsonResponse(data, safe=False)

    