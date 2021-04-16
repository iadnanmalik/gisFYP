from django.shortcuts import render, redirect
from .models import PakAdm3
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from TS2 import simulation,weapongeneration, HaversineDistance, RangeEfficiency, calculateTimeToThreat
import pandas as pd
from fyp import getThreatIndex

weaponsdata=[]
for i in range(0,5):
    weaponsdata.append(weapongeneration(i))
model = pd.read_pickle(r'E:\FYP\FYP code\gisFYP\new_model.pickle')


def index(request):
    return render(request, 'gisapp/index.html')
def PakData(request):
    pakdata=serialize('geojson',PakAdm3.objects.all())
    return HttpResponse(pakdata,content_type='geojson')
def getSimulatorData(request):
    Lat,Long,angles,threatscore,threatid,threatspeed,ammunition,altitude,name,rangee=simulation()
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
        # print(weaponsdata[i])
        weaponwisedistance=[]
        for j in range (len(Lat)):
            weaponwisedistance.append(HaversineDistance(weaponsdata[i].wlongitude,weaponsdata[i].wlatitude,Long[j],Lat[j],altitude,weaponsdata[i].waltitude))
        distancebyweapons.append(weaponwisedistance)
    threatInrange=[]
    weaponsthreats=[]
    for j in range (len(Lat)):
        threatByWeapon=[]
        for i in range(len(weaponsdata)):
            if(weaponsdata[i].wmaxrange>distancebyweapons[i][j] and weaponsdata[i].wmaxrange/6<distancebyweapons[i][j] ):
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
    print(timeFrame)
    for i in range(len(timeFrame)):
        print("At time frame ",i," We have ",len(timeFrame[i])," options")
        #pass
    check= True
    threatHealth.append(10)
    for i in range(len(finalResult)):
        if(finalResult[i][1]!=-1):
            if(threatHealth[i]>0):            
                health=threatHealth[i]-finalResult[i][1]
                threatHealth.append(health)
            else:
                threatHealth.append(threatHealth[i])
         
        else:
            threatHealth.append(threatHealth[i])
         
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

    return JsonResponse(data)
"""
#boundaries for THreats
[60.89943695068354,29.83749580383312],
[62.5035400390625,29.376403808593807],
[64.91727447509766,29.556589126586857],
[65.87509918212902,29.743312835693473],
[66.09905242919916,29.282470703125],
[64.83136749267584,28.734996795654297],
[63.93742752075195,28.40848159790039],
[62.802379608154354,27.88588905334484],
[61.39097213745123,29.21361160278326],
[61.383487701416016,29.221462249755973]

#Defended Assets
28.959660, 63.411098
28.967538, 64.645676
29.339287, 64.392563
28.581572, 62.761875
29.365385, 61.573407

#Weapon Systems
28.959661, 63.411097
28.967539, 64.645677
29.339288, 64.392562
28.581573, 62.761874
29.365386, 61.573408



"""