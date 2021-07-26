from django.urls import path
from data import views

urlpatterns = [
    path('get_threats/', views.get_threats),
]