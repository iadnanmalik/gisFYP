from django.shortcuts import render, redirect
from .models import PakAdm3,WeaponLoc, DefendedAssetLoc,SimulatorEssential
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from TS2 import simulation,weapongeneration, HaversineDistance, RangeEfficiency, calculateTimeToThreat, weaponsInfo
import pandas as pd
from fyp import getThreatIndex
import requests
import json
# Machine Learning Model
model = pd.read_pickle(r'E:\FYP\FYP code\gisFYP\new_model.pickle')

# Same weapons for every reload
weaponsdata=[]
weaponsdata=weaponsInfo()

# Referring to the main index page
def index(request):
    return render(request, 'gisapp/index.html')

# Data containing the geographical features of Pakistan
def PakData(request):
    pakdata=serialize('geojson',PakAdm3.objects.all())
    return HttpResponse(pakdata,content_type='geojson')

# Loading the weapons from the Database 
def weapons(request): 
    weapon_db=WeaponLoc.objects.all()
    weaponsreq=serialize('json',weapon_db)
    return JsonResponse(weaponsreq,safe=False)

# Loading defended assets from the Database 
def defendedassets(request):
    assests_db=DefendedAssetLoc.objects.all()
    assetsreq=serialize('json',assests_db)
    return JsonResponse(assetsreq,safe=False)

# Loading the information required for simulation from the Database
def simulationInfo(request):
    records= SimulatorEssential.objects.all()
    recordsreq=serialize('json',records)
    return JsonResponse(recordsreq,safe=False)

# Main Simulation Fuction
def getSimulatorData(request):
    
    # Requesting API for plane initials
    response= requests.get("http://localhost:8000/get_threats/")
    obj=response.json()
    res_lat=float(obj["lat"])
    res_lon=float(obj["lon"])
    res_angle=int(obj["angle"])

    # Passing the plane initials and getting multiple necessary params in return
    Lat,Long,angles,threatscore,threatid,threatspeed,ammunition,altitude,name,rangee=simulation(res_lat,res_lon,res_angle)
    threatIndex=[]
  
    # Getting threat Index of each plane
    for i in range (len(Lat)):
        threatIndex.append(getThreatIndex(Lat[i],Long[i],threatscore,threatid,threatspeed,ammunition,altitude,rangee))
        
   
    finalThreatIndex=[]
    # Final threat Index is the max of all the threat indexes proposed by all Defended Assets
    for i in range(len(threatIndex)):
        maxval=max(threatIndex[i])
        finalThreatIndex.append(maxval)
    
    distancebyweapons=[]
    weaponwisedistance=[]
    # In a 2D each weapon to all threats distance is stored
    for i in range(len(weaponsdata)):
        
        weaponwisedistance=[]
        for j in range (len(Lat)):
            weaponwisedistance.append(HaversineDistance(weaponsdata[i].wlongitude,weaponsdata[i].wlatitude,Long[j],Lat[j],altitude,weaponsdata[i].waltitude))
        distancebyweapons.append(weaponwisedistance)
    threatInrange=[]
    weaponsthreats=[]
    for j in range (len(Lat)):
        threatByWeapon=[]
    #    Preparing the information we have for Kill Probability Prediction
        for i in range(len(weaponsdata)):
            if(weaponsdata[i].wmaxrange>distancebyweapons[i][j] and weaponsdata[i].wmaxrange/9<distancebyweapons[i][j] ):
                weaponrange=RangeEfficiency(distancebyweapons[i][j],weaponsdata[i].wmaxrange) 
                status=weaponsdata[i].wstatus
                previousperformance= weaponsdata[i].wpreviousperformance
                wammo = weaponsdata[i].wammuniation
                wfamiliarity= weaponsdata[i].wfamiliarity
                wTimeToThreat=calculateTimeToThreat(weaponsdata[i].wspeed,distancebyweapons[i][j])
                tIndex= finalThreatIndex[j]
                # The result of the prediction is the Kill Probability
                result = model.predict([[weaponrange,status,previousperformance,wammo,wfamiliarity,wTimeToThreat,tIndex]])
              
                result= float(result)
                threatByWeapon.append([weaponrange,status,previousperformance,wammo,wfamiliarity,wTimeToThreat,tIndex,result,i])
        weaponsthreats.append(threatByWeapon)
    finalResult=[]
    threatHealth =[]
    timeFrame=[]
 
    # Storing the Max kill Probability, Weapon Indexes and Indexes of weapons at TimeFrames
 
    for i in range(len(weaponsthreats)):
 
        maxssp=-1
        maxindex=-1
        singleTimeFrame=[]
 
        for j in range (len(weaponsthreats[i])):
 
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
        finalResult.append([i,maxssp,maxindex])
    
    # Introducing the threat health and calculating it for each time frame just for the sake of simulation
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
  
    # The range of weapons is given so that the circles can be drawn in simulation
    weaponRange=[]
    for i in range(len(weaponsdata)):
        weaponRange.append(weaponsdata[i].wmaxrange)
  
    # Data is passed to index.html in form of json response
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
