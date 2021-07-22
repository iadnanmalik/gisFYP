from django.contrib import admin
from django.urls import path,include
from .views import index,PakData,getSimulatorData,defendedassets, simulationInfo,weapons
urlpatterns = [
 
    path('',index,name='index'),
    path('pakdata',PakData,name='pakdata'),
    path('weapons',weapons,name='weapons'),
    path('defendedassets',defendedassets,name='defendedassets'),
    path('getSimulatorData',getSimulatorData,name='getSimulatorData'),
    path('simulationInfo',simulationInfo,name='simulationInfo')
]
