#!/usr/bin/env python
# coding: utf-8


import numpy as np


# ## This function serves the purpose of calculating distance on the basis of Longitude and Latitude 


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
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
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
print("The Flying Distane between Lahore & Islamabad is :",HaversineDistance(long1,lat1,long2,lat2,alt1),"KMs")


# ## Distance incorporating latitude

#alt1 - altitude of a threat
#alt2 - reference alttiude considering it to be zero(sea- level)
#Moderate	1200-2400m / 4000-7870 ft
#High	2400-4000m / 7870-13,125 ft
#Very High	4000-5500m / 13,125-18,000 ft


# ## Class of an AirCraft

class ThreatAirCraft:
    #velocity : speed at an instance T
    #latitude and longtitude : the position of the aircraft at an instant T
    #Threat Score: the terror imparted by the AirCraft (0-10)
    #CarriedWeapon: The ammunition being carried by the aircraft(0-10) - 0 mean no issue
    #Altitude: Determines that where the threat is ? is it flying at low height or high height? Reference point is considered 0m
    def __init__(self,Id,name,Type,Model,v,alt,lat,lon,tS,CW):
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
    def GetAircraftData(self):
      '''  print("--------AIRCRAFT--------\nID:"
             ,self.AirCraftID
            ,"\nUser Defined Name:",self.AirCraftName
            ,"\nType:",self.AirCraftType
            ,"\nVelocity:",self.Velocity,"KM/s"
            ,"\nAltitude:",self.altitude,"Ms"
            ,"\nLatitude:",self.latitude
            ,"\nLongtitude:",self.longtitude
            ,"\nThreatScore:",self.ThreatScore
            ,"\nCarriedWeapon:",self.CarriedWeapon)
        '''
T1=ThreatAirCraft(1221,"Titan1","Interceptor",2011,10000,5000,11.5204,94.3587,1,0)
T2=ThreatAirCraft(1222,"Titan2","Interceptor",2012,20000,4000,35.6260,73.0714,2,2)
T3=ThreatAirCraft(1223,"Titan3","Interceptor",2013,30000,3000,31.5204,74.3587,3,3)
T4=ThreatAirCraft(1224,"Titan4","Interceptor",2014,40000,2000,41.5204,64.3587,4,4)
T5=ThreatAirCraft(1225,"Titan5","Interceptor",2015,50000,1200,51.5204,54.3587,5,5)
T6=ThreatAirCraft(1226,"Titan6","Interceptor",2016,60000,1000,61.5204,44.3587,6,6)
T7=ThreatAirCraft(1227,"Titan7","Interceptor",2017,70000,2200,71.5204,34.3587,7,7)
T8=ThreatAirCraft(1228,"Titan8","Interceptor",2018,80000,1100,81.5204,24.3587,8,8)
T9=ThreatAirCraft(1229,"Titan9","Interceptor",2019,90000,1770,91.5204,14.3587,9,9)
T10=ThreatAirCraft(12210,"Titan10","Interceptor",2020,100000,1123,31.5204,74.3587,10,10)
ThreatsContainer=[T1,T2,T3,T4,T5,T6,T7,T8,T9,T10]
#T1.GetAircraftData()
for i in range(10):
    ThreatsContainer[i].GetAircraftData()
    


# ## Class of The Defended Assets


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
        
   # def GetDefendedAssetData(self):
        #print("-----Defended Asset-----\nID:",self.DefendedAssetID,"\nDefendedAsset:",self.DefendedAsset,
         #     "\nLatitude:",self.latitude,"\nLongtitude:",self.lontitude,"\nVitality:",self.Vitality
          #    )
        
DA1=DefendedAsset(112231,"Sargodha Base",32.0455,72.6716,3)
DA2=DefendedAsset(112232,"GHQ",33.6260,73.0714,4)
DA3=DefendedAsset(112233,"PMA",34.1887,73.2633,5)
DA4=DefendedAsset(112234,"Naval Base",24.8400,66.9742,6)
DA5=DefendedAsset(112235,"Chashma Nuclear Complex",32.3874,71.4685,7)
DefendedAssetsContainer=[DA1,DA2,DA3,DA4,DA5]

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
    #print("distance",s)
    #Velocity of the Aircraft
    #KEEP EVEYTHING IN KMs
    v=T1.Velocity
    
    #time in reaching to a certain destination
    t= (s/v) # time is in hours since velocity is in km/h
    
    #### division by zero dekhnay ke zarurat ha ####
    
    #print("time",t)
    #*3600 #seconds
    #print("Time Left :",t*360)
    #calculating threat index
    if T1.CarriedWeapon<=0:
        TIndex=0
    else:
        TIndex =  (((T1.CarriedWeapon)+(T1.ThreatScore) + (DA1.Vitality) )/(2*t))
    
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
    
ThreatEvaluationBetweenSingleThreatSingleDefendedAsset(DA1,T1)


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
    


ThreatEvaluation(DefendedAssetsContainer,ThreatsContainer)
#0 wo threat ha jis k pas weapon he nae
#high means height pa ha
#low kam height pa
#moderate darmeani height pa

print("Check Titan2")
print(ThreatEvaluation(DefendedAssetsContainer,ThreatsContainer))
#0 wo threat ha jis k pas weapon he nae
#high means height pa ha
#low kam height pa
#moderate darmeani height pa

def getThreatIndex(lat,lon,threatscore,threatid,threatspeed,ammunition,altitude):
    threat=ThreatAirCraft(threatid,"Titan1","Interceptor",2011,threatspeed,altitude,lat,lon,threatscore,0)
    #1221,"Titan1","Interceptor",2011,10000,5000,11.5204,94.3587,1,0
    threatindex=[]
    tind=ThreatEvaluation(DefendedAssetsContainer,threat)
    #print(tind)
    for key, value in tind.items(): 
        print (key, value) 
        threatindex.append(value)
        print("\n")
    
    nthreatindex=[]
    return threatindex



