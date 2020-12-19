# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 21:59:47 2020

@author: Rawan
"""
import random
import time
import math
from gisapp.models import ThreatValue
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

def threatgeneration():

     ID = ['1001','1002','1003','1101','3002','3003''4002','4003']
     name=['Cargo','Bomber','MIG-21','MIG-25','F-15','F-16','MIG-19','MIG-23']
     model=['2001','2002','2003','2005','2006','2007','2014','2010']
     typ=['Rotorcraft','FixedWing','JetCraft','PropellerCraft']
     lat=[27.4888,30.3222,31.2555,33.10,36.40]  #lat
     lon=[71.8666,69.8888,74.1999,73.74,69.93] #lon
     ID1=ThreatValue.objects.values('id')
     name1=ThreatValue.objects.values('name')
     model1=ThreatValue.objects.values('model')
     typ1=ThreatValue.objects.values('typ')
     name1list=[]
     rangee=random.randrange(300,700,50)
     angle=random.randint(0,360)
     threatscore =random.randint(1,7)
     speed=random.randint(300,500)
     ammuniation=random.randint(0,5)
     for names in name1: 
        #print (key, value) 
        name1list.append(names['name'])
        #print("\n")
     print(name1list)
     ID1list=[]
     print(ID1)
     for ids in ID1: 
        #print (key, value) 
        ID1list.append(ids['id'])
        #print("\n")
     print(ID1list)
     model1list=[]
     for models in model1: 
        #print (key, value) 
        model1list.append(models['model'])
        #print("\n")
     print(model1list)
     typ1list=[]
     for typs in typ1: 
        #print (key, value) 
        typ1list.append(typs['typ'])
        #print("\n")
     print(typ1list)
     ID=ID1list
     name=name1list
     model=model1list
     typ=typ1list
     
     threatid=random.choice(ID)
     ID.remove(threatid)
     namee=random.choice(name)
     typee=random.choice(typ)
     mod=random.choice(model)
     index=random.randint(0,4)
     l1=lon[index]
     l2=lat[index]
     altitude=random.randint(1000,5000)
     new=Threat(threatid,namee,mod,typee,threatscore,speed,l2,l1,rangee,angle,ammuniation,altitude)
     return new
def simulation():
    threat=threatgeneration()
    l1=threat.longitude
    l2=threat.latitude
    t=1
    angle=threat.angle
    latitude=[]
    longitude=[]
    angles=[]
    #speed=random.randint(350,450)
    distance =threat.speed/7
        
    for i in range (0,10):
        lon1=l1*(math.pi/180)
        lat1=l2*(math.pi/180)
        angrad= angle * (math.pi/180)   #angle in radian
        lat=math.asin(math.sin(lat1)*math.cos(distance/radius)+math.cos(lat1)*math.sin(distance/radius)*math.cos(angrad))
        lon=lon1+math.atan2(math.sin(angrad)*math.sin(distance/radius)*math.cos(lat1),
                          math.cos(distance/radius)-math.sin(lat1)*math.sin(lat))
        t+=7          #refreshing time
        llon=lon * (180/math.pi)
        llat=lat * (180/math.pi)
        l1=llon
        l2=llat
        ang= angrad * (180/math.pi)  #angle in degree
        
        print("longitude:",llon)
        print("latitude:",llat)
        print("angle:",ang)
        latitude.append(llat)
        longitude.append(llon)
        angles.append(angle)

        angle+=10
    return latitude,longitude,angles,threat.threatscore,threat.ID,threat.speed,threat.ammuniation,threat.altitude,threat.name
def main():
    t=1
    threat=threatgeneration()
    print(threat)
    simulation()
    
if __name__ == '__main__':
    main()
