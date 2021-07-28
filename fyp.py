import numpy as np
from gisapp.models import DefendedAssetLoc
from math import radians, cos, sin, asin, sqrt
import numpy as np
from math import radians, cos, sin, asin, sqrt

# This file gives us the threatIndex

# ## This function serves the purpose of calculating distance on the basis of Longitude and Latitude 
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





class Threat:
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


def ThreatEvaluation(DefendedAssets,EncounteredThreats):
    #This is a key value pair 
    DefendedAssetAndThreatIndex={}
    # Threat Evaluatio between threats and defended assets is performed
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
    

# This function calls all of the above functions to calculate threat index
def getThreatIndex(lat,lon,threatscore,threatid,threatspeed,ammunition,altitude,rangee):
    threatindex=[]

    #print("------------------------Range-----------------------------")
    #print(rangee)
    threat=Threat(threatid,"Titan1","Interceptor",2011,threatspeed,altitude,lat,lon,threatscore,ammunition,rangee)
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


