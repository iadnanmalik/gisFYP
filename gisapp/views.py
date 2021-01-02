from django.shortcuts import render, redirect
from .models import PakAdm3
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from TS2 import simulation
from fyp import getThreatIndex
def index(request):
    return render(request, 'gisapp/index.html')
def PakData(request):
    pakdata=serialize('geojson',PakAdm3.objects.all())
    return HttpResponse(pakdata,content_type='geojson')
def getSimulatorData(request):
    Lat,Long,angles,threatscore,threatid,threatspeed,ammunition,altitude,name=simulation()
    #ammunition=0
    threatIndex=[]
    for i in range (len(Lat)):
        threatIndex.append(getThreatIndex(Lat[i],Long[i],threatscore,threatid,threatspeed,ammunition,altitude))
    #print("Threat Index Printing")
    #print(threatIndex)
    finalThreatIndex=[]
    for i in range(len(threatIndex)):
        maxval=max(threatIndex[i])
        finalThreatIndex.append(maxval)
    #print(finalThreatIndex)


    data={
        "Lat":Lat,
        "Long":Long,
        "angles":angles,
        "threatIndex":finalThreatIndex,
        "threatScore":threatscore,
        "name":name,
        "CarriedWeapon":ammunition
    }

    return JsonResponse(data)