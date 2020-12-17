from django.contrib import admin
from django.urls import path,include
from .views import index,PakData,getSimulatorData
urlpatterns = [
 
    path('',index,name='index'),
    path('pakdata',PakData,name='pakdata'),
    path('getSimulatorData',getSimulatorData,name='getSimulatorData')
]
