from django.shortcuts import render, redirect
from .models import PakAdm3,WeaponLoc, DefendedAssetLoc,SimulatorEssential
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from TS2 import simulation,weapongeneration, HaversineDistance, RangeEfficiency, calculateTimeToThreat, weaponsInfo
import pandas as pd
from fyp import getThreatIndex
import requests
import json

model = pd.read_pickle(r'E:\FYP\FYP code\gisFYP\new_model.pickle')
weaponsdata=[]
weaponsdata=weaponsInfo()


def index(request):
    return render(request, 'gisapp/index.html')
def PakData(request):
    pakdata=serialize('geojson',PakAdm3.objects.all())
    return HttpResponse(pakdata,content_type='geojson')

def weapons(request): 
    weapon_db=WeaponLoc.objects.all()
    weaponsreq=serialize('json',weapon_db)
    return JsonResponse(weaponsreq,safe=False)

def defendedassets(request):
    assests_db=DefendedAssetLoc.objects.all()
    assetsreq=serialize('json',assests_db)
    return JsonResponse(assetsreq,safe=False)

def simulationInfo(request):
    records= SimulatorEssential.objects.all()
    recordsreq=serialize('json',records)
    return JsonResponse(recordsreq,safe=False)

def getSimulatorData(request):
    response= requests.get("http://localhost:8000/get_threats/")
    obj=response.json()
    res_lat=float(obj["lat"])
    res_lon=float(obj["lon"])
    res_angle=int(obj["angle"])

    Lat,Long,angles,threatscore,threatid,threatspeed,ammunition,altitude,name,rangee=simulation(res_lat,res_lon,res_angle)
    #ammunition=0
    threatIndex=[]
    for i in range (len(Lat)):
        threatIndex.append(getThreatIndex(Lat[i],Long[i],threatscore,threatid,threatspeed,ammunition,altitude,rangee))
        
    #print("Threat Index Printing")
    #print(threatIndex)
    finalThreatIndex=[]
    for i in range(len(threatIndex)):
        maxval=max(threatIndex[i])
        finalThreatIndex.append(maxval)
    #print(finalThreatIndex)

    distancebyweapons=[]
    weaponwisedistance=[]
    #print(weaponsdata[0].wlatitude)
    for i in range(len(weaponsdata)):
        #print(weaponsdata[i])
        weaponwisedistance=[]
        for j in range (len(Lat)):
            weaponwisedistance.append(HaversineDistance(weaponsdata[i].wlongitude,weaponsdata[i].wlatitude,Long[j],Lat[j],altitude,weaponsdata[i].waltitude))
        distancebyweapons.append(weaponwisedistance)
    threatInrange=[]
    weaponsthreats=[]
    for j in range (len(Lat)):
        threatByWeapon=[]
        for i in range(len(weaponsdata)):
            if(weaponsdata[i].wmaxrange>distancebyweapons[i][j] and weaponsdata[i].wmaxrange/9<distancebyweapons[i][j] ):
                weaponrange=RangeEfficiency(distancebyweapons[i][j],weaponsdata[i].wmaxrange) 
                status=weaponsdata[i].wstatus
                previousperformance= weaponsdata[i].wpreviousperformance
                wammo = weaponsdata[i].wammuniation
                wfamiliarity= weaponsdata[i].wfamiliarity
                wTimeToThreat=calculateTimeToThreat(weaponsdata[i].wspeed,distancebyweapons[i][j])
                tIndex= finalThreatIndex[j]

                result = model.predict([[weaponrange,status,previousperformance,wammo,wfamiliarity,wTimeToThreat,tIndex]])
                #print(weaponrange,status,previousperformance,wammo,wfamiliarity,wTimeToThreat,tIndex,result)
                result= float(result)
                threatByWeapon.append([weaponrange,status,previousperformance,wammo,wfamiliarity,wTimeToThreat,tIndex,result,i])
        weaponsthreats.append(threatByWeapon)
    finalResult=[]
    threatHealth =[]
    timeFrame=[]
    #singleTimeFrame = []
    #print(weaponsthreats)
    
    #---------------Normalization-------------------------
    #for i in range(len(weaponsthreats)):
     #   for j in range(len(weaponsthreats[i])):
      #      weaponsthreats[i][j][len(weaponsthreats[i][j])-2]= ( weaponsthreats[i][j][len(weaponsthreats[i][j])-2]-1)/(10-1)
    
    
    
    for i in range(len(weaponsthreats)):
        #print(len(weaponsthreats[i]))
        #print("Frame number",i)
        maxssp=-1
        maxindex=-1
        singleTimeFrame=[]
        for j in range (len(weaponsthreats[i])):
          #  print("Weapon Number",j, " Will hit Threat at Time Frame ",i, )
            if(j==0): 
                maxssp=weaponsthreats[i][j][len(weaponsthreats[i][j])-2]
                maxindex=weaponsthreats[i][j][len(weaponsthreats[i][j])-1]
                
                singleTimeFrame.append([maxssp,maxindex])
            else:
                if(weaponsthreats[i][j][len(weaponsthreats[i][j])-2]>maxssp):
                    maxssp=weaponsthreats[i][j][len(weaponsthreats[i][j])-2]
                    maxindex=weaponsthreats[i][j][len(weaponsthreats[i][j])-1]
                    singleTimeFrame.append([maxssp,maxindex])
                else:
                    singleTimeFrame.append([weaponsthreats[i][j][len(weaponsthreats[i][j])-2],weaponsthreats[i][j][len(weaponsthreats[i][j])-1]])
        timeFrame.append(singleTimeFrame)
        #print("Max One SSP ",maxssp, " and Weapon Number ", maxindex)
        #print(weaponsthreats[i])
        finalResult.append([i,maxssp,maxindex])
    #print(timeFrame)
    #for i in range(len(timeFrame)):
    #    for j in range(len(timeFrame[i])):
            #timeFrame[i][j][0]= ( timeFrame[i][j][0])/(10)
        #pass
    #print(finalResult)

    for i in range(len(finalResult)):
        if(i==0):
            if(finalResult[i][1]!=-1):
                threatHealth.append(15-finalResult[i][1])
            else:
                threatHealth.append(15)
        else:
            if(finalResult[i][1]!=-1):
                if(threatHealth[i-1]>0):            
                    health=threatHealth[i-1]-finalResult[i][1]
                    threatHealth.append(health)
                else:
                    threatHealth.append(threatHealth[i-1])
            
            else:
                threatHealth.append(threatHealth[i-1])
   # for i in range(len(finalResult)):
   #       finalResult[i][1]= ( finalResult[i][1])/(10)
    
    #print(threatHealth)
    #print(finalResult)
    weaponRange=[]
    for i in range(len(weaponsdata)):
        weaponRange.append(weaponsdata[i].wmaxrange)
    #print(weaponRange)
    data={
        "Lat":Lat,
        "Long":Long,
        "angles":angles,
        "threatIndex":finalThreatIndex,
        "threatScore":threatscore,
        "name":name,
        "CarriedWeapon":ammunition,
        "speed": threatspeed,
        "weaponsResult": finalResult,
        "weaponsRange":weaponRange,
        "threatHealth": threatHealth,
        "timeFrame":timeFrame
    }
    #print(threatHealth)
    #print(finalResult)
    #print(len(weaponsdata))
    return JsonResponse(data)
