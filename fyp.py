#!/usr/bin/env python
# coding: utf-8


import numpy as np

from gisapp.models import DefendedAssetLoc
# ## This function serves the purpose of calculating distance on the basis of Longitude and Latitude 


from math import radians, cos, sin, asin, sqrt

import numpy as np

from math import radians, cos, sin, asin, sqrt

def HaversineDistance(lon1, lat1, lon2, lat2,alt1,alt2=0):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6378.1 # Radius of earth in kilometers. Use 3956 for miles
    d=c*r
    alt1=alt1/1000 #converting altitude in KMs
    h=alt1-alt2
    distance = sqrt( d**2+ h**2)
    
    return distance
#coordintes of lahore
lat1=33.6844
long1 =73.0479
#coordinates of isb
lat2=31.5204 
long2=74.3587
alt1=4000
#print("The Flying Distane between Lahore & Islamabad is :",HaversineDistance(long1,lat1,long2,lat2,alt1),"KMs")




#alt1 - altitude of a threat
#alt2 - reference alttiude considering it to be zero(sea- level)
#Moderate	1200-2400m / 4000-7870 ft
#High	2400-4000m / 7870-13,125 ft
#Very High	4000-5500m / 13,125-18,000 ft




class ThreatAirCraft:
    #velocity : speed at an instance T
    #latitude and longtitude : the position of the aircraft at an instant T
    #Threat Score: the terror imparted by the AirCraft (0-7)
    #CarriedWeapon: The ammunition being carried by the aircraft(0-15) - 0 mean no issue
    #Altitude: Determines that where the threat is ? is it flying at low height or high height? Reference point is considered 0m
    def __init__(self,Id,name,Type,Model,v,alt,lat,lon,tS,CW,Rng):
        self.AirCraftID=Id
        self.AirCraftName=name
        self.AirCraftType=Type
        self.AirCraftModel=Model
        self.Velocity=v
        self.altitude=alt
        self.latitude=lat
        self.longtitude=lon
        self.ThreatScore=tS
        self.CarriedWeapon=CW
        self.Range=Rng
    def GetAircraftData(self):
        print("--------AIRCRAFT--------\nID:"
             ,self.AirCraftID
            ,"\nUser Defined Name:",self.AirCraftName
            ,"\nType:",self.AirCraftType
            ,"\nVelocity:",self.Velocity,"KM/h"
            ,"\nAltitude:",self.altitude,"Ms"
            ,"\nLatitude:",self.latitude
            ,"\nLongtitude:",self.longtitude
            ,"\nThreatScore:",self.ThreatScore
            ,"\nCarriedWeapon:",self.CarriedWeapon
             ,"\nMaxRange:",self.Range,"Kms")
        
T1=ThreatAirCraft(1221,"Titan1","Interceptor",2011,3000,5000,42.0455,78.6716,8,8,2100)
T2=ThreatAirCraft(1222,"Mig-21","Interceptor",2012,2000,4000,21.5204,84.3587,2,2,3000)
T3=ThreatAirCraft(1223,"Thunder","Interceptor",2013,2500,3000,31.5204,74.3587,3,3,1500)
T4=ThreatAirCraft(1224,"Bolt-4","Interceptor",2014,3000,2000,41.5204,64.3587,4,4,2000)
T5=ThreatAirCraft(1225,"Intruder","Interceptor",2015,1400,1200,51.5204,54.3587,5,5,3500)
T6=ThreatAirCraft(1226,"F-16","Interceptor",2016,1700,1000,61.5204,44.3587,6,6,2500)
T7=ThreatAirCraft(1227,"Hawker","Interceptor",2017,2100,2200,71.5204,34.3587,7,7,2300)
T8=ThreatAirCraft(1228,"P-51","Interceptor",2018,2700,1100,81.5204,24.3587,8,8,2200)
T9=ThreatAirCraft(1229,"Tupolev","Interceptor",2019,2200,1770,91.5204,14.3587,9,9,3700)
T10=ThreatAirCraft(12210,"Hurricane","Interceptor",2720,1100,1123,31.5204,74.3587,10,10,4000)
ThreatsContainer=[T1,T2,T3,T4,T5,T6,T7,T8,T9,T10]
#T1.GetAircraftData()
#for i in range(10):
 #   ThreatsContainer[i].GetAircraftData()
    




class DefendedAsset:
    #lat
    #long
    #id
    #name
    #vitality: value ranging between 0-10
    def __init__(self,Id,name,lat,long,vital):
        self.DefendedAssetID=Id
        self.DefendedAsset=name
        self.lontitude=long
        self.latitude=lat
        self.Vitality=vital
        
    def GetDefendedAssetData(self):
        print(" ")
        #print("-----Defended Asset-----\nID:",self.DefendedAssetID,"\nDefendedAsset:",self.DefendedAsset,
           #   "\nLatitude:",self.latitude,"\nLongtitude:",self.lontitude,"\nVitality:",self.Vitality
            #  )
        
DA1=DefendedAsset(112231,"Sargodha Base",28.959660, 63.411098,6)
DA2=DefendedAsset(112232,"GHQ",28.967538, 64.645676,8)
DA3=DefendedAsset(112233,"PMA",29.339287, 64.392563,10)
DA4=DefendedAsset(112234,"Naval Base",28.581572, 62.761875,12)
DA5=DefendedAsset(112235,"Chashma Nuclear Complex",29.365385, 61.573407,14)

#assests_db=DefendedAssetLoc.objects.all()
#for item in assests_db:
#    asset= DefendedAsset(int(item.id),str(item.name),float(item.lat),float(item.lon),)
assests_db=DefendedAssetLoc.objects.all()
DefendedAssetsContainer=[]

for item in assests_db:
    asset= DefendedAsset(int(item.id),str(item.name),float(item.lat),float(item.lon),int(item.vitality))
    DefendedAssetsContainer.append(asset)
    

#for i in range(5):
 #   DefendedAssetsContainer[i].GetDefendedAssetData()


# ## Function to calculate Threat Index


#Takes input 
#distance
#velocity of aircraft
#heading angle of aircraft
#Threat score
#Returns Threat Index
#S=v*t 
#on the basis of time we shall decide what to do ?
#DA1 will be containing the lats and longs and vitality 
#T1 will be containing lats, longs, velocity, threat score, WE MAY ADD OTHER THINGS TOO but rn for the sake of
#simplicity we wont consider the weapon load and stuff like that

def ThreatEvaluationBetweenSingleThreatSingleDefendedAsset(DA1,T1):
    
    #distance between the DA and the Aircraft
    s=HaversineDistance(DA1.lontitude, DA1.latitude, T1.longtitude, T1.latitude,T1.altitude) #Kms
    ##print("distance",s)
    #Velocity of the Aircraft
    #KEEP EVEYTHING IN KMs
    v=T1.Velocity
    
    #time in reaching to a certain destination
    t= (s/v) # time is in hours since velocity is in km/h
    #print("Time= ",t)
    #### division by zero dekhnay ke zarurat ha ####

    ##print("time",t)
    #*3600 #seconds
    ##print("Time Left :",t*360)
    #calculating threat index
    TIndex=0
    if T1.CarriedWeapon<=0:
        TIndex=0
    else:
        try:
            
            maxV=10/3500      
            TindexMaxAssumed=((10+10+4500+10)/maxV)
            

            TIndex =  (((T1.CarriedWeapon/10)+(T1.ThreatScore/7)  +(T1.Range/4000)+(DA1.Vitality/7) )/(t/2))
            #TIndex =  (((T1.CarriedWeapon)+(T1.ThreatScore) + (DA1.Vitality) ))
            #TIndex =  (((T1.CarriedWeapon) + (DA1.Vitality) )/(2*t))
            import math 
            # #printing the log base 2 of TI 
            TIndex=math.log(TIndex,2)
            ##print("Max TI | ",TIndex)
           
        except:
            print("Yahan pa max value daal dayn gay ")
    ThreatAndAsset=T1.AirCraftName+"-->"+DA1.DefendedAsset
    #Moderate	1200-2400m / 4000-7870 ft
    #High	2400-4000m / 7870-13,125 ft
    #Very High	4000-5500m / 13,125-18,000 ft
    if T1.altitude<2400:
        ThreatAndAsset+="-->"
        ThreatAndAsset+="Low"
        
    elif T1.altitude<4000:
        ThreatAndAsset+="-->"
        ThreatAndAsset+="Moderate"
    else:
        ThreatAndAsset+="-->"
        ThreatAndAsset+="High"
        
    return ThreatAndAsset,TIndex
    
#ThreatEvaluationBetweenSingleThreatSingleDefendedAsset(DA1,T1)
##print("Ammunition =",T1.CarriedWeapon,"| Terror Of Threat =",T1.ThreatScore,"| DA Vitality =",DA1.Vitality)
##print("Threat Index =",ThreatEvaluationBetweenSingleThreatSingleDefendedAsset(DA1,T1))



#This function will take 2 lists , 1 will be the list of DAs the other will be a list of Threats.
#Intuition here is that the Radar(Simulator) will return an array of encountered threats and DAs

def normalize(d,a,b):
    
    mini=min(d.values())
    if mini ==0:
        for key,value in d.items():
            if mini<value:
                mini =value
                break
    # division by zero dekhnay ke zarurat ha
    maxi=max(d.values())
    #maxi=17344827
    dif=maxi-mini
    rang=b-a
    for key,value in d.items():
        if value!=0:
            d[key]=(((((value-mini)/dif)*rang)+a))
        else:
            d[key]=0
            
    return d
def ThreatEvaluation(DefendedAssets,EncounteredThreats):
    #This is a key value pair 
    DefendedAssetAndThreatIndex={}
    for assets in DefendedAssets:
        if type(EncounteredThreats)!=list:
                Aandt,Tind=ThreatEvaluationBetweenSingleThreatSingleDefendedAsset(assets,EncounteredThreats)
                DefendedAssetAndThreatIndex[Aandt]=Tind
        else:
            for threats in EncounteredThreats:
                Aandt,Tind=ThreatEvaluationBetweenSingleThreatSingleDefendedAsset(assets,threats)
                DefendedAssetAndThreatIndex[Aandt]=Tind
    #normalise the value of dicitonary between 0 and 7
    #DefendedAssetAndThreatIndex=normalize(DefendedAssetAndThreatIndex,1.0,7.0)
    return DefendedAssetAndThreatIndex
    

##print(ThreatEvaluation(DefendedAssetsContainer,ThreatsContainer),'\n')
##print(ThreatsContainer[0].GetAircraftData())
    
def getThreatIndex(lat,lon,threatscore,threatid,threatspeed,ammunition,altitude,rangee):
    threatindex=[]

    #print("------------------------Range-----------------------------")
    #print(rangee)
    threat=ThreatAirCraft(threatid,"Titan1","Interceptor",2011,threatspeed,altitude,lat,lon,threatscore,ammunition,rangee)
    #print(threat.GetAircraftData())   
    #1221,"Titan1","Interceptor",2011,10000,5000,11.5204,94.3587,1,0
    tind=ThreatEvaluation(DefendedAssetsContainer,threat)
    ##print(tind)
    for key, value in tind.items(): 
        #print (key, value) 
        threatindex.append(value)
        ##print("\n")
    #print("TIndex ",threatindex) 
    return threatindex


