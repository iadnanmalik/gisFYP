
import random
import time
import math
from math import radians, cos, sin, asin, sqrt

from gisapp.models import WeaponLoc
from gisapp.models import ThreatValue
from gisapp.models import SimulatorEssential
radius= 6378.1


class Threat:

    def __init__(self, ID,name,model,typee,ts,speed,lat,lon,rangee,angle,ammuniation,altitude):
        self.ID =ID
        self.name = name
        self.model = model
        self.type = typee
        self.threatscore = ts
        self.speed = speed
        self.latitude = lat
        self.longitude = lon
        self.maxrange= rangee
        self.angle=angle
        self.ammuniation= ammuniation
        self.altitude=altitude

    def __str__(self):
        return " ThreatID: '{}' | ThreatName: '{}'  | Type: {} | ModelYear: {} | ThreatScore: {} | Speed: {} km/s | Latitude: {} | Longitude: {} | MaxRange: {} km | InitialAngle: {} degrees |CarriedAmmuniation: {} \n"\
            .format(self.ID, self.name,self.type, self.model, self.threatscore, self.speed,self.latitude,self.longitude,self.maxrange,self.angle,self.ammuniation)

    def __repr__(self):
        return str(self)

# Generating a threat 
def threatgeneration(lat,lon,angle):
     ID1=ThreatValue.objects.values('id')
     name1=ThreatValue.objects.values('name')
     model1=ThreatValue.objects.values('model')
     typ1=ThreatValue.objects.values('typ')
     name1list=[]
     rangee=random.randrange(1000,4000,50)
     threatscore =random.randint(1,7)
     speed=random.randint(1000,3000)
     ammuniation=random.randint(0,10)
     for names in name1: 
        #print (key, value) 
        name1list.append(names['name'])
        #print("\n")
     #print(name1list)
     ID1list=[]
     #print(ID1)
     for ids in ID1: 
        ##print (key, value) 
        ID1list.append(ids['id'])
        ##print("\n")
     #print(ID1list)
     model1list=[]
     for models in model1: 
        ##print (key, value) 
        model1list.append(models['model'])
        ##print("\n")
     #print(model1list)
     typ1list=[]
     for typs in typ1: 
        ##print (key, value) 
        typ1list.append(typs['typ'])
        ##print("\n")
     #print(typ1list)
     ID=ID1list
     name=name1list
     model=model1list
     typ=typ1list
     
     threatid=random.choice(ID)
     ID.remove(threatid)
     namee=random.choice(name)
     typee=random.choice(typ)
     mod=random.choice(model)
     

     dummy=angle
     dummy2=dummy+90
     angle=random.randint(dummy,dummy2)

     altitude=random.randint(15000,20000)
     new=Threat(threatid,namee,mod,typee,threatscore,speed,lat,lon,rangee,angle,ammuniation,altitude)
     return new

# Simulation creates path for the threats
def simulation(lat,lon,angle):
    threat=threatgeneration(lat,lon,angle)
    l1=threat.longitude
    l2=threat.latitude
    t=1
    angle=threat.angle
    latitude=[]
    longitude=[]
    angles=[]
    #speed=random.randint(350,450)
    kmpersecond=threat.speed/15
    distance =kmpersecond/3
    simulationTime=SimulatorEssential.objects.values('simulationTime')
    time=0
    for rec in simulationTime:
        time=rec['simulationTime']
    
    for i in range (0,time):
        lon1=l1*(math.pi/180)
        lat1=l2*(math.pi/180)
        angrad= angle * (math.pi/180)   #angle in radian
        # Next Latittude and Longitude
        lat=math.asin(math.sin(lat1)*math.cos(distance/radius)+math.cos(lat1)*math.sin(distance/radius)*math.cos(angrad))
        lon=lon1+math.atan2(math.sin(angrad)*math.sin(distance/radius)*math.cos(lat1),
                          math.cos(distance/radius)-math.sin(lat1)*math.sin(lat))
        t+=7          #refreshing time
        llon=lon * (180/math.pi)
        llat=lat * (180/math.pi)
        # Updating new latitudes and Longitudes
        l1=llon
        l2=llat
        ang= angrad * (180/math.pi)  #angle in degree
        
        #print("longitude:",llon)
        #print("latitude:",llat)
        #print("angle:",ang)
        latitude.append(llat)
        longitude.append(llon)
        angles.append(angle)

        angle+=10
    return latitude,longitude,angles,threat.threatscore,threat.ID,threat.speed,threat.ammuniation,threat.altitude,threat.name, threat.maxrange
class Weapon:

    def __init__(self, WID,wname,alt,wspeed,lat,lon,rangee,wangle,trav,wammuniation,ammshot,deptime,wstatus,previousperformance,wfamiliarity):
        self.WID =WID
        self.wname = wname
        self.waltitude=alt
        self.wspeed = wspeed
        self.wlatitude = lat
        self.wlongitude = lon
        self.wmaxrange= rangee
        self.wangle=wangle
        self.wtraverse=trav
        self.wammuniation= wammuniation
        self.wammuniationshot=ammshot
        self.wdeploytime=deptime
        self.wstatus=wstatus
        self.wpreviousperformance= previousperformance
        self.wfamiliarity= wfamiliarity
    def __str__(self):
        return " WeaponWID: '{}' | Weaponwname: '{}'  | waltitude : {} m | Muzzle Velocity: {} km/s | wlatitude: {} | wlongitude: {} | wmaxrange: {} km | Elevationwangle: {} degrees |wtraversewangle: {} degrees |Carriedwammuniation: {} | RateofFire: {} | DeploymentTime: {} secs | Weaponwstatus: {}  \n"            .format(self.WID, self.wname,self.waltitude, self.wspeed,self.wlatitude,self.wlongitude,self.wmaxrange,self.wangle,self.wtraverse,self.wammuniation,self.wammuniationshot,self.wdeploytime,self.wstatus)

    def __repr__(self):
        return str(self)

def weapongeneration(lat,lon):
    
    WID = ['001','002','003','004','005','006','007']
    wname=['W1','W2','W3','W4','W5','W6','W7']
    #lat=[32.0456,32.0466,33.6261,33.6271,34.1888,34.1897,24.8401,24.8411,32.3875,32.3885]  #wlatitude of fire # Place alongside defended assests
    #lon=[72.6717,72.6727,73.0715,73.0725,73.2634,73.2644,66.9743,66.9753,71.4686,71.4696] #wlongitude of fire
    wangle=random.randint(0,90)
    trav=random.randint(0,360)
    #rangee=random.randrange(1000,5000,50)  #range of fire
    wangle=random.randint(0,90) #elevation wangle
    wspeed=random.randint(3000,4000)
    waltitude=random.randint(0,2000)
    wammuniation=random.uniform(0,100)
    noofamm=random.randint(1,3) #rate of fire #Range is upto 120000 thats why we can eliminate this in final dataset
    deploymenttime=random.randint(1,10)
    wstatus=random.randint(0,1)
    af= math.radians(wangle)

    rangee=(((wspeed**2)*math.sin(2*45))/127008)
    weaponid=WID[0]
    #WID.remove(weaponid)  #removing for unique id
    wnamee=wname[0]
    #index=random.randint(0,4)
    wPreviousPerformance=random.randint(1,10)
    wfamiliarity= random.randint(1,10)

        
    new=Weapon(weaponid,wnamee,waltitude,wspeed,lat,lon,rangee,wangle,trav,wammuniation,noofamm,deploymenttime,wstatus,wPreviousPerformance,wfamiliarity)
    return new
# The function to return list of weapons on calling
def weaponsInfo():
    weapon_db=WeaponLoc.objects.all()
    weaponsLat=[]
    weaponsLon=[]
    weapondata=[]
    for item in weapon_db:
        weaponsLat.append(float(item.lat))
        weaponsLon.append(float(item.lon))
    for i in range(len(weaponsLat)):
        weapondata.append(weapongeneration(weaponsLat[i],weaponsLon[i]))
    return weapondata


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
    alt2=alt2/1000
    h=alt1-alt2
    distance = sqrt( d**2+ h**2)
    
    return distance

# THe function to calculate the optimal range of hitting from weapon to threat
def RangeEfficiency(Distance,maxRange):
    # The minimum range a weapon can hit
    minRange=maxRange/6
    # Optimal range of hitting
    optimalRange=(maxRange+minRange)/2
    if Distance >= optimalRange and Distance < maxRange:
        # Efficient range of hitting the threat if it hasn't cross half way to the threat
        Efficiency = optimalRange/Distance
        return Efficiency 
    elif Distance <= optimalRange and Distance > minRange:
        # Efficient range of hitting the threat if it has crossed half way to the threat
        Efficiency = optimalRange/(Distance+(optimalRange-Distance)*2)
        return Efficiency
    else:
        return 0

def calculateTimeToThreat(weaponVelocity,distanceFromThreat):
    #s=v*t
    #t=s/v
    #v in km/h
    #s in kms
    return distanceFromThreat/weaponVelocity
